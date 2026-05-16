from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import HouseholdInformationTable, MemberInformationTable, LightingFeeTable, LightingRecordTable
from datetime import date

class LightingSystemTests(APITestCase):

    def setUp(self):
        """
        創建資料庫
        """
        # 先建立一個空的戶口 (此時戶長為 None)
        self.household = HouseholdInformationTable.objects.create(
            Household_ID="H001",
            phone="0912345678"
        )

        # 建立信徒並關聯到該戶口
        self.head_member = MemberInformationTable.objects.create(
            Member_ID="M001", 
            name="戶長張三",
            Household_ID=self.household
        )

        # 回頭更新戶口的戶長為該信徒
        self.household.Head_of_Household_ID = self.head_member
        self.household.save()

        # 建立燈種
        self.lamp_gm = LightingFeeTable.objects.create(Lamp_Type_ID="L001", Lamp_Type="光明燈", Price=600)
        self.lamp_ts = LightingFeeTable.objects.create(Lamp_Type_ID="L002", Lamp_Type="太歲燈", Price=800)

    # --- LGT-003: 查詢功能測試 ---
    def test_search_lighting_record(self):
        # 建立一筆預設紀錄
        LightingRecordTable.objects.create(
            Lighting_Record_ID="R001",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm,
            Year=2024,
            Lamp_Lighting_Date=date.today()
        )
        
        # 測試：使用電話搜尋
        url = reverse('light:search_lighting_record')
        response = self.client.get(url, {'phone': '0912345678', 'year': 2024})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['Data']), 1)
        self.assertEqual(response.data['Data'][0]['Member_Name'], "戶長張三")

    # --- LGT-002: 顯示全科目狀態測試 ---
    def test_member_lighting_status(self):
        # 測試：取得信徒點燈狀態 (目前應該全為未點)
        url = reverse('light:member_lighting_status', kwargs={'member_id': 'M001'})
        response = self.client.get(url, {'year': 2024})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 預期會有兩個燈種，且 Is_Lit 都是 False
        self.assertEqual(len(response.data['Data']), 2)
        self.assertFalse(response.data['Data'][0]['Is_Lit'])

    # --- LGT-001: 建立點燈紀錄測試 ---
    def test_create_lighting_record(self):
        url = reverse('light:create_lighting_record')
        data = {
            "Data": {
                "Household_ID": "H001",
                "Member_ID": "M001",
                "Lamp_Type_IDs": ["L001", "L002"],
                "Year": 2024
            }
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 驗證 API 是否「成功建立了資料」。
        self.assertEqual(response.data['Data']['Total_Fee'], 1400) # 600 + 800
        # 驗證回傳的總金額是否正確。

    # --- LGT-002: 更新點燈紀錄測試 ---
    def test_update_lighting_record(self):
        # 先建立一筆點燈紀錄
        record = LightingRecordTable.objects.create(
            Lighting_Record_ID="R_OLD",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm,# L001 
            Year=2024,
            Lamp_Lighting_Date=date.today()
        )
        
        # 測試：把光明燈(L001)改成太歲燈(L002)
        url = reverse('light:update_lighting_record', kwargs={'lighting_record_id': 'R_OLD'})
        data = {
            "Data": {
                "Year": 2024,
                "Member_ID": "M001",
                "Lamp_Type_ID": "L002"
            }
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Data']['Lamp_Type'], "太歲燈")

    # --- 取消/刪除點燈紀錄測試 ---
    def test_delete_lighting_record(self):
        # 先建立一筆紀錄
        record = LightingRecordTable.objects.create(
            Lighting_Record_ID="R_TO_DELETE",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm,
            Year=2024,
            Lamp_Lighting_Date=date.today()
        )
        
        url = reverse('light:delete_lighting_record', kwargs={'lighting_record_id': 'R_TO_DELETE'})
        data = { "Data": { "Member_ID": "M001" } }
        response = self.client.delete(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(LightingRecordTable.objects.filter(Lighting_Record_ID="R_TO_DELETE").exists())
    
    # --- LGT-004: 計算費用與繳費流程測試 ---
    def test_calculate_lighting_fee_with_details(self):
        # 建立兩筆紀錄
        r1 = LightingRecordTable.objects.create(
            Lighting_Record_ID="R1", Household_ID=self.household, Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm, Year=2024, Lamp_Lighting_Date=date.today()
        )
        r2 = LightingRecordTable.objects.create(
            Lighting_Record_ID="R2", Household_ID=self.household, Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_ts, Year=2024, Lamp_Lighting_Date=date.today()
        )

        url = reverse('light:calculate_lighting_fee')
        data = { "Data": { "Lighting_Record_IDs": ["R1", "R2"] } }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Total_Amount'], 1400)
        self.assertEqual(len(response.data['Details']), 2)
        self.assertEqual(response.data['Details'][0]['Member_Name'], "戶長張三")

    def test_create_lighting_payment_updates_records(self):
        # 建立一筆紀錄
        record = LightingRecordTable.objects.create(
            Lighting_Record_ID="R_PAY", Household_ID=self.household, Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm, Year=2024, Lamp_Lighting_Date=date.today()
        )

        url = reverse('light:create_lighting_payment')
        data = {
            "Data": {
                "Lighting_Record_IDs": ["R_PAY"],
                "Household_ID": "H001"
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 驗證紀錄是否被標記為已繳費
        record.refresh_from_db()
        self.assertTrue(record.is_paid)
        self.assertIsNotNone(record.payment_ref)


# --- LGT-005: 匯出點燈清冊測試 ---
    def test_export_lighting_inventory(self):
        # 1. 準備測試資料 (建立一筆 2026 年的紀錄)
        LightingRecordTable.objects.create(
            Lighting_Record_ID="R_2026",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm,
            Year=2026,
            Lamp_Lighting_Date=date.today()
        )

        url = reverse('light:export_lighting_inventory')
        
        # 測試情境 1: 篩選年份 (2026)
        response = self.client.get(url, {'year': 2026})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['Data']), 1)
        self.assertEqual(response.data['Data'][0]['Member_ID'], "M001")
        # 驗證是否有包含要求的「更新日期」欄位
        self.assertIn('Updated_Date', response.data['Data'][0])

        # 測試情境 2: 篩選燈種 (L001)
        response = self.client.get(url, {'lamp_type_id': 'L001'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['Data']), 1)

        # 測試情境 3: 篩選日期 (未來或過去的日期過濾)
        response = self.client.get(url, {'start_date': '2026-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# --- LGT-006: 燈條列印預覽與確認測試 ---

    def test_light_strip_preview(self):
        """測試燈條預覽：應只顯示已繳費的紀錄"""
        # 1. 建立一筆「已繳費」的紀錄
        r_paid = LightingRecordTable.objects.create(
            Lighting_Record_ID="R_PAID",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm,
            Year=2026,
            Lamp_Lighting_Date=date.today(),
            is_paid=True  # 設定為已繳費
        )
        
        # 2. 建立一筆「未繳費」的紀錄 (不應出現在預覽中)
        r_unpaid = LightingRecordTable.objects.create(
            Lighting_Record_ID="R_UNPAID",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_ts,
            Year=2026,
            Lamp_Lighting_Date=date.today(),
            is_paid=False # 未繳費
        )

        # 呼叫預覽 API (手動加入 url，因為原本 urls.py 可能尚未定義，建議確認 urls.py 是否有對應名稱)
        # 假設 path 名稱為 'light:light_strip_preview'
        url = reverse('light:light_strip_preview') 
        response = self.client.get(url, {'year': 2026})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 預期結果：只有 1 筆 (已繳費的那筆)
        self.assertEqual(len(response.data['Data']), 1)
        self.assertEqual(response.data['Data'][0]['Lighting_Record_ID'], "R_PAID")
        # 檢查是否有產生格式化的顯示字串 (Display_Text)
        self.assertIn("Display_Text", response.data['Data'][0])

    def test_light_strip_print_confirm(self):
        """測試確認列印：更新資料庫狀態為已列印"""
        # 1. 準備一筆已繳費但未列印的紀錄
        record = LightingRecordTable.objects.create(
            Lighting_Record_ID="R_PRINT_ME",
            Household_ID=self.household,
            Member_ID=self.head_member,
            Lamp_Type_ID=self.lamp_gm,
            Year=2026,
            Lamp_Lighting_Date=date.today(),
            is_paid=True,
            print_status='not_printed' # 初始狀態
        )

        url = reverse('light:light_strip_print_confirm')
        data = {
            "Data": {
                "Lighting_Record_IDs": ["R_PRINT_ME"]
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Status'], "Success")
        
        # 2. 驗證資料庫狀態是否真的改變了
        record.refresh_from_db()
        from .models import PrintStatus
        self.assertEqual(record.print_status, PrintStatus.PRINTED)
