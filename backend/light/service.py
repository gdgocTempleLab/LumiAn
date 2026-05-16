from .models import LightingFeeTable
from .models import LightingRecordTable

def calculate_total_fee(lamp_type_ids):
    """
    計算所選燈種的總費用
    """
    if not lamp_type_ids:
        return 0
        
    # 取得所有選中的燈種價格
    prices = LightingFeeTable.objects.filter(
        Lamp_Type_ID__in=lamp_type_ids
    ).values_list('Price', flat=True)
    
    return sum(prices)



"""
根據給定的紀錄 ID 列表，計算各類型燈種數量與總金額
"""
def get_lighting_payment_summary(record_ids):

    records = LightingRecordTable.objects.filter(Lighting_Record_ID__in=record_ids)
    
    total_amount = 0
    guangming_count = 0
    taisui_count = 0
    
    details = []
    for record in records:
        # 累加金額 (假設 Lamp_Type_ID 關聯對象有 Price 欄位)
        total_amount += record.Lamp_Type_ID.Price
        
        # 判斷燈種名稱
        lamp_name = record.Lamp_Type_ID.Lamp_Type
        if "光明燈" in lamp_name:
            guangming_count += 1
        elif "太歲燈" in lamp_name:
            taisui_count += 1
            
        # 加入詳細資訊
        details.append({
            "Lighting_Record_ID": record.Lighting_Record_ID,
            "Member_Name": record.Member_ID.name,
            "Lamp_Type": lamp_name,
            "Price": record.Lamp_Type_ID.Price
        })
            
    return {
        "GuangMing_Count": guangming_count,
        "TaiSui_Count": taisui_count,
        "Total_Amount": total_amount,
        "Details": details
    }
    

def generate_lighting_inventory_data(records):
    """
    將點燈紀錄 QuerySet 轉換為清冊格式
    格式：戶員 ID (Member_ID), 更新日期 (Record_Updated_Time)
    """
    inventory_list = []
    for record in records:
        inventory_list.append({
            "Member_ID": record.Member_ID.Member_ID,
            "Member_Name": record.Member_ID.name, # 額外附上姓名增加可讀性
            "Lamp_Type": record.Lamp_Type_ID.Lamp_Type,
            "Updated_Date": record.Record_Updated_Time.strftime('%Y-%m-%d %H:%M:%S') if record.Record_Updated_Time else None,
            "Year": record.Year
        })
    return inventory_list


def generate_light_strip_content(records):
    """
    LGT-006: 顯示燈條列印內容
    """
    print_list = []
    # 準備一個空清單，等等要裝整理好的資料
    for record in records:
        # 一筆一筆處理點燈紀錄
        member = record.Member_ID # 點燈的人。
        household = record.Household_ID # 戶籍資料。
        
        # 格式化農曆生日 (若無則顯示未填寫)
        lunar_bday = member.Lunar_Birthday.strftime('%Y-%m-%d') if member.Lunar_Birthday else "未填寫"
        
        # 固定格式內容
        formatted_content = {
            "Lighting_Record_ID": record.Lighting_Record_ID,
            "Member_Name": member.name,
            "Lunar_Birthday": lunar_bday,
            "Address": household.Address or "未填寫",
            "Lamp_Type": record.Lamp_Type_ID.Lamp_Type,
            "Year": record.Year,
            # 產生一個組合好的字串供快速預覽/列印
            "Display_Text": f"{record.Year}年度 {record.Lamp_Type_ID.Lamp_Type} | {member.name} | 農曆:{lunar_bday} | {household.Address or ''}"
        }
        print_list.append(formatted_content)
    return print_list

def mark_records_as_printed(record_ids):
    # 傳進來一串點燈紀錄 ID（可能是多筆）
    """
    LGT-006: 將點燈紀錄標示為「已列印」
    """
    from .models import PrintStatus
    # 從 model 匯入 PrintStatus
    updated_count = LightingRecordTable.objects.filter(
        Lighting_Record_ID__in=record_ids
    ).update(print_status=PrintStatus.PRINTED)
    # 將狀態更新成已列印。
    
    return updated_count
    # 回傳總共更新了幾筆