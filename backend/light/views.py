#使用者送出「戶號 + 信徒 + 想點的燈種 + 年份」
#系統驗證資料(檢查 response 有沒有這個資料-->看看DB有沒有這個資料)
#幫信徒建立點燈紀錄
#計算總金額
#回傳成功結果

from uuid import uuid4
from datetime import date
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # Django REST Framework 的核心
from believer.models import Household_Information, Member_Information
from .models import (
    LightingFeeTable,
    LightingRecordTable,
    LightingPaymentTable
)

from light.service import (
    calculate_total_fee,
    get_lighting_payment_summary,
    generate_light_strip_content,
    mark_records_as_printed
)

# ==========================================
# 新增點燈紀錄
# ==========================================


class CreateLightingRecordAPIView(APIView):

    permission_classes = [] #不用登入即可新增，這部分應該要改，需要加入登入驗證

    def post(self, request): 

        data = request.data.get("Data", {}) #Response 用來回傳 JSON。
        
        # 取得欄位，把資料拆出來，JSON資料原本都放在一起，現在把它拆出來
        household_id = data.get("Household_ID")
        member_id = data.get("Member_ID")
        lamp_type = data.get("Lamp_Type")  # 單個燈種（新的前端方式）
        lamp_type_ids = data.get("Lamp_Type_IDs", [])  # 保持相容舊方式
        year = data.get("Year")
        amount = data.get("Amount", 0)  # 新增: 金額
        notes = data.get("Notes", "")  # 新增: 備註

        # =====================================
        # 檢查 request.data 裡有沒有這個欄位
        # =====================================

        if not household_id: # 確認有輸入戶口
            return Response({
                "Status": "Error",
                "Message": "Household_ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not member_id: # 確認有輸入信徒
            return Response({
                "Status": "Error",
                "Message": "Member_ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not lamp_type and not lamp_type_ids:# 確認有輸入燈種
            return Response({
                "Status": "Error",
                "Message": "Lamp_Type or Lamp_Type_IDs is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not year: #確認有輸入年份
            return Response({
                "Status": "Error",
                "Message": "Year is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # =====================================
        # 查詢戶口(確認database 有沒有這筆資料)
        # =====================================

        household = Household_Information.objects.filter( # 避免重複點燈
            Household_ID=household_id
        ).first()

        if not household:
            return Response({
                "Status": "Error",
                "Message": "Household not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # =====================================
        # 查詢信徒
        # =====================================

        member = Member_Information.objects.filter(
            Member_ID=member_id,
            Household__Household_ID=household.Household_ID
        ).first()

        if not member:
            return Response({
                "Status": "Error",
                "Message": "Member not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # =====================================
        # 建立點燈紀錄
        # =====================================

        created_records = []
        
        # 支援新舊兩種方式
        lamp_types_to_create = [lamp_type] if lamp_type else lamp_type_ids

        for lamp_type_id in lamp_types_to_create:

            lamp_type_obj = LightingFeeTable.objects.filter(
                Lamp_Type_ID=lamp_type_id
            ).first()

            if not lamp_type_obj:
                continue

            # 避免重複點燈，檢查這位信徒今年是否已點過這盞燈。
            exists = LightingRecordTable.objects.filter(
                Member_ID=member,
                Lamp_Type_ID=lamp_type_obj,
                Year=year
            ).exists()

            if exists:
                continue #如果已經點過，就跳過這個loop，不再新增

            record = LightingRecordTable.objects.create(
                Lighting_Record_ID=str(uuid4()),
                Household_ID=household,
                Member_ID=member,
                Lamp_Type_ID=lamp_type_obj,
                Year=year,
                Lamp_Lighting_Date=date.today(),
                Amount=amount,  # 新增: 金額
                Notes=notes,  # 新增: 備註
            )

            created_records.append({
                "Lighting_Record_ID": record.Lighting_Record_ID,
                "Lamp_Type": lamp_type_obj.Lamp_Type,
                "Price": lamp_type_obj.Price,
                "Amount": record.Amount,
                "Notes": record.Notes,
            })

        # =====================================
        # 計算總費用
        # =====================================

        total_fee = calculate_total_fee(lamp_types_to_create)

        # =====================================
        # 回傳結果
        # =====================================

        return Response({
            "Status": "Success",
            "Message": "Lighting records created successfully.",
            "Data": {
                "Member_Name": member.name,
                "Year": year,
                "Records": created_records,
                "Total_Fee": total_fee
            }
        }, status=status.HTTP_201_CREATED)



# ================================================
# 使用者使用電話或戶長查詢點燈紀錄
# ================================================

class SearchLightingRecordAPIView(APIView):

    permission_classes = []

    def get(self, request):
        # 獲取參數：從 URL 的查詢字串（Query Parameters）中取得 phone、head_name、year。
        phone = request.GET.get("phone")
        head_name = request.GET.get("head_name") # 戶長姓名
        year = request.GET.get("year")
        is_paid = request.GET.get("is_paid") # 新增：可過濾已繳費/未繳費

        records = LightingRecordTable.objects.all() 
        #初步查詢：先取出所有的資料 LightingRecordTable.objects.all()（這時還沒執行 SQL，Django 採用 Lazy Evaluation）。

        # 電話查詢:使用 __icontains 進行模糊比對，並透過 Household_ID__phone 跨表查詢住戶電話。
        if phone:
            records = records.filter(
                Household_ID__phone__icontains=phone
            )

        # 戶長查詢:
        # 這是一個三層跨表查詢：從點燈紀錄 -> 住戶（Household） 戶長（Head of Household） -> 姓名
        if head_name:
            records = records.filter(
                Household_ID__Head_of_Household_ID__name__icontains=head_name
            )

        # 年份查詢:精確比對 Year 欄位。
        if year:
            records = records.filter(
                Year=year
            )

        # 繳費狀態查詢:
        if is_paid is not None:
            is_paid_bool = is_paid.lower() in ['true', '1', 'yes']
            records = records.filter(is_paid=is_paid_bool)
        else:
            # 預設查詢時，通常前端想看的是「所有」或「未繳費」？
            # 這裡我們保持彈性，如果有傳才過濾。
            pass

        result = [] #回傳：回傳 JSON 格式，包含狀態與結果資料。

        for record in records: # 手動序列化：透過 for 迴圈將 QuerySet 物件轉換為 Python 字典清單。

            result.append({
                "Lighting_Record_ID": record.Lighting_Record_ID,
                "Household_ID": record.Household_ID.Household_ID, # 戶號
                "Member_ID": record.Member_ID.Member_ID, 
                # API 需要 Member_ID 才能查出全科目清單。如果搜尋結果沒給 ID，前端就沒辦法呼叫下一個 API。
                "Member_Name": record.Member_ID.name,
                "Lamp_Type": record.Lamp_Type_ID.Lamp_Type,
                "Year": record.Year,
                "Phone": record.Household_ID.phone,
                "Is_Paid": record.is_paid, # 新增回傳欄位
                "Amount": record.Amount, # 新增: 金額
                "Notes": record.Notes or "", # 新增: 備註
                "Record_Creation_Time": record.Record_Creation_Time.isoformat() if record.Record_Creation_Time else "",
                "Record_Updated_Time": record.Record_Updated_Time.isoformat() if record.Record_Updated_Time else "",
            })

        return Response({
            "Status": "Success",
            "Data": result
        })


# LGT-002 編輯點燈紀錄================================
# 查詢並顯示所有點燈清單  
class MemberLightingStatusAPIView(APIView):
    """
    回傳該信徒在特定年份的所有燈種狀態。
    前端可以拿這個清單來顯示「哪些點了、哪些沒點」。
    """
    permission_classes = []

    def get(self, request, member_id):
        # 從 URL 參數獲取年份，預設為今年
        year = request.GET.get("year", date.today().year)
        
        # 1. 撈出資料庫中所有的燈種 
        all_lamp_types = LightingFeeTable.objects.all()
        
        # 2. 撈出該信徒在該年份已經點過的紀錄
        existing_records = LightingRecordTable.objects.filter(
            Member_ID=member_id,
            Year=year
        )
        
        # 建立一個對照表 {燈種ID: 紀錄物件}，方便等一下比對
        record_map = {r.Lamp_Type_ID.Lamp_Type_ID: r for r in existing_records}
        
        result = []
        for lamp in all_lamp_types:
            # 檢查這個燈種是否在已點清單中
            record = record_map.get(lamp.Lamp_Type_ID)
            
            result.append({
                "Lamp_Type_ID": lamp.Lamp_Type_ID,
                "Lamp_Type": lamp.Lamp_Type,
                "Price": lamp.Price,
                "Is_Lit": record is not None,  # True 代表已點，False 代表未點
                "Lighting_Record_ID": record.Lighting_Record_ID if record else None,
                "Lamp_Lighting_Date": record.Lamp_Lighting_Date if record else None,
            })

        return Response({
            "Status": "Success",
            "Member_ID": member_id,
            "Year": year,
            "Data": result
        })

# ================================================
# 編輯並儲存點燈紀錄
# 使用者修改點燈資訊
# 系統更新資料
# ================================================

class UpdateLightingRecordAPIView(APIView): # put

    permission_classes = [] # 權限設定(目前不需要登入)

    def put(self, request, lighting_record_id): # 更新資料
        # self這是 Python 類別（Class）函式的標準參數，代表這個 API 物件本身。
        # request:包含了前端送過來的所有資訊，例如：request.data：前端送來的 JSON 資料（新的燈種、年份等）。request.user：目前是誰在操作（如果有登入的話）。
        # lighting_record_id:URL（網址） 傳進來的參數(ex:/api/light/update/LGT-12345/)，後端靠這個 ID 才知道「到底是哪一筆紀錄」要被修改。

        data = request.data.get("Data", {}) # 接收前端資料

        # 拆解前端送來的資料 
        year = data.get("Year") 
        member_id = data.get("Member_ID") 
        new_lamp_type_id = data.get("Lamp_Type_ID")
        amount = data.get("Amount")  # 新增: 金額
        is_paid = data.get("Is_Paid")  # 新增: 繳費狀態
        notes = data.get("Notes")  # 新增: 備註

        # 查詢 record ， 去資料庫找 這筆點燈紀錄 ID、年份
        record = LightingRecordTable.objects.filter(
            Lighting_Record_ID=lighting_record_id
        ).first()

        if not record: # 如果找不到資料，就回傳錯誤
            return Response({
                "Status": "Error",
                "Message": "找不到該筆點燈紀錄"
            }, status=status.HTTP_404_NOT_FOUND)

        # 若只有部分欄位要更新（例如只改金額或繳費狀態，不改燈種），則允許通過
        if new_lamp_type_id:
            # 3. 驗證身分：確保這筆紀錄真的屬於這位信徒
            if record.Member_ID.Member_ID != member_id:
                return Response({
                    "Status": "Error", 
                    "Message": "信徒身分不符，無法修改他人的紀錄"
                }, status=status.HTTP_403_FORBIDDEN)
            # 4. 驗證年份
            if str(record.Year) != str(year):
                return Response({"Status": "Error", "Message": "年份不符合"}, status=status.HTTP_400_BAD_REQUEST)
            # 5. 查詢新燈種是否存在
            lamp_type = LightingFeeTable.objects.filter(Lamp_Type_ID=new_lamp_type_id).first()
            if not lamp_type:
                return Response({"Status": "Error", "Message": "找不到該燈種"}, status=status.HTTP_404_NOT_FOUND)

            # 檢查是否重複
            exists = LightingRecordTable.objects.filter(
                Member_ID=record.Member_ID,
                Lamp_Type_ID=lamp_type,
                Year=year
            ).exclude(
                Lighting_Record_ID=record.Lighting_Record_ID
            ).exists()

            # 如果重複，就回傳錯誤
            if exists:
                return Response({
                    "Status": "Error",
                    "Message": "This lamp has already been registered."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 更新燈種
            record.Lamp_Type_ID = lamp_type

        # 新增：允許更新其他欄位
        if amount is not None:
            record.Amount = amount
        if is_paid is not None:
            record.is_paid = is_paid
        if notes is not None:
            record.Notes = notes

        # 更新時間
        record.Record_Updated_Time = timezone.now()

        record.save()#儲存資料

        return Response({ # 回傳成功訊息
            "Status": "Success",
            "Message": "Lighting record updated successfully.",
            "Data": {
                "Lighting_Record_ID": record.Lighting_Record_ID,
                "Lamp_Type_ID": record.Lamp_Type_ID.Lamp_Type_ID if record.Lamp_Type_ID else None,
                "Lamp_Type": record.Lamp_Type_ID.Lamp_Type if record.Lamp_Type_ID else None,
                "Amount": record.Amount,
                "Is_Paid": record.is_paid,
                "Notes": record.Notes,
                "Updated_Time": record.Record_Updated_Time
            }
        }, status=status.HTTP_200_OK)

# 取消點燈紀錄
class DeleteLightingRecordAPIView(APIView):
    """
    刪除點燈紀錄 (取消點燈)
    """
    permission_classes = []

    def delete(self, request, lighting_record_id):
        # 1. 取得這筆紀錄
        record = LightingRecordTable.objects.filter(
            Lighting_Record_ID=lighting_record_id
        ).first()

        if not record:
            return Response({
                "Status": "Error",
                "Message": "找不到該筆點燈紀錄"
            }, status=status.HTTP_404_NOT_FOUND)

        # 2. (選擇性) 驗證身分：確保不能亂刪別人的紀錄
        # 如果前端有傳 Member_ID 過來，可以進行比對
        member_id = request.data.get("Data", {}).get("Member_ID")
        if member_id and record.Member_ID.Member_ID != member_id:
            return Response({
                "Status": "Error",
                "Message": "身分不符，無法刪除此紀錄"
            }, status=status.HTTP_403_FORBIDDEN)

        # 3. 正式刪除
        record.delete()

        return Response({
            "Status": "Success",
            "Message": "點燈紀錄已成功刪除 (已取消點燈)"
        }, status=status.HTTP_200_OK)

# ===========================================
"""
LGT-004 計算點燈費用
"""
class CalculateLightingFeeAPIView(APIView):
    """
    計算費用試算 (不寫入資料庫):
    讓前端使用者點選要繳費的項目後，先計算出總金額、各類燈種數量，但不會修改資料庫。
    """
    def post(self, request):
        # request 就是使用者點選要計算的點燈紀錄，傳送 requst到後端
        record_ids = request.data.get('Data', {}).get('Lighting_Record_IDs', [])
        # 從 request.data 中提取 Data 物件裡的 Lighting_Record_IDs
        if not record_ids: # 如果沒有提供任何 ID，回傳 400 Bad Request 錯誤。
            return Response({"error": "未提供紀錄 ID"}, status=status.HTTP_400_BAD_REQUEST)
        # 1. 計算金額給前端的使用者看，不會傳到後端計入DB
        summary = get_lighting_payment_summary(record_ids) 
        """
        呼叫 get_lighting_payment_summary(record_ids) 函式。
        這個函式通常定義在 service.py 中，它會根據 ID 去查詢資料庫，加總「光明燈」、「太歲燈」等的數量與金額。
        """
        return Response(summary, status=status.HTTP_200_OK)

class CreateLightingPaymentAPIView(APIView):
    """確認繳費並建立記錄"""
    def post(self, request):
        data = request.data.get('Data', {})
        record_ids = data.get('Lighting_Record_IDs', [])
        household_id = data.get('Household_ID')
        
        if not record_ids or not household_id:
            return Response({"error": "缺少必要資訊"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. 為了防止前端會被亂改，所以後端也要再計算一次
        summary = get_lighting_payment_summary(record_ids)
        
        # 2. 獲取住戶實例
        try:
            household = Household_Information.objects.get(Household_ID=household_id)
        except Household_Information.DoesNotExist:
            return Response({"error": "找不到指定住戶"}, status=status.HTTP_404_NOT_FOUND)
        
        # 3. 建立支付紀錄
        payment = LightingPaymentTable.objects.create(
            Household_ID=household,
            GuangMing_Count=summary['GuangMing_Count'],
            TaiSui_Count=summary['TaiSui_Count'],
            Total_Amount=summary['Total_Amount']
        )

        # 4. 更新點燈紀錄狀態 (標記為已繳費並關聯支付單)
        LightingRecordTable.objects.filter(Lighting_Record_ID__in=record_ids).update(
            is_paid=True,
            payment_ref=payment
        )
        
        return Response({
            "status": "success",
            "Payment_ID": payment.Payment_ID,
            "summary": summary
        }, status=status.HTTP_201_CREATED)

"""
LGT-005 匯出點燈清冊
支援篩選條件：年份、燈種 ID、開始日期、結束日期
"""
class ExportLightingInventoryAPIView(APIView):

    permission_classes = []

    def get(self, request):
        # 取得篩選參數
        year = request.GET.get("year")
        lamp_type_id = request.GET.get("lamp_type_id")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # 基礎查詢
        records = LightingRecordTable.objects.all()

        # 套用篩選條件
        if year:
            records = records.filter(Year=year)
        if lamp_type_id:
            records = records.filter(Lamp_Type_ID=lamp_type_id)

        if start_date and end_date:
            records = records.filter(Record_Updated_Time__date__range=[start_date, end_date])
        elif start_date:
            records = records.filter(Record_Updated_Time__date__gte=start_date)

        # 依照更新日期排序 (由新到舊)
        records = records.order_by('-Record_Updated_Time')

        # 整理清冊資料
        from .service import generate_lighting_inventory_data
        inventory_data = generate_lighting_inventory_data(records)

        return Response({
            "Status": "Success",
            "Count": len(inventory_data),
            "Data": inventory_data
        }, status=status.HTTP_200_OK)

"""
 LGT-006: 燈條列印預覽
"""

class LightStripPreviewAPIView(APIView):
    permission_classes = []
    def get(self, request):
        year = request.GET.get("year")
        if not year:
            return Response({
                "Status": "Error",
                "Message": "Year is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # 查詢該年度已繳費且未列印的紀錄 (通常已繳費才列印)
        records = LightingRecordTable.objects.filter(
            Year=year,
            is_paid=True
        ).order_by('Record_Creation_Time')

        # 產生預覽資料
        preview_data = generate_light_strip_content(records)

        return Response({
            "Status": "Success",
            "Year": year,
            "Count": len(preview_data),
            "Data": preview_data
        }, status=status.HTTP_200_OK)


"""
LGT-006: 確認列印並更新狀態
"""

class LightStripPrintConfirmAPIView(APIView):

    permission_classes = []

    def post(self, request):
        # 接收前端的 request
        data = request.data.get("Data", {})
        # 抓取 request 中的 Lighting_Record_IDs
        record_ids = data.get("Lighting_Record_IDs", [])
        # 如果 request 中的 Lighting_Record_IDs 為空，回傳 400 Bad Request
        if not record_ids:
            return Response({
                "Status": "Error",
                "Message": "Lighting_Record_IDs are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新狀態為「已列印」
        updated_count = mark_records_as_printed(record_ids)

        # 再次取得這些紀錄的列印內容供最終確認輸出
        records = LightingRecordTable.objects.filter(Lighting_Record_ID__in=record_ids)
        print_output = generate_light_strip_content(records)

        return Response({
            "Status": "Success",
            "Message": f"Successfully marked {updated_count} records as printed.",
            "Print_Output": print_output
        }, status=status.HTTP_200_OK)
