#!/usr/bin/env python
"""初始化點燈數據"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lumian.settings')
django.setup()

from light.models import LightingFeeTable, LightingRecordTable
from believer.models import Household_Information, Member_Information
from datetime import date
from uuid import uuid4

# 初始化燈種數據
lamp_types = [
    ('LT001', '光明燈', 500),
    ('LT002', '太歲燈', 1000),
    ('LT003', '藥師燈', 700),
    ('LT004', '財神燈', 800),
    ('LT005', '文昌燈', 600),
    ('LT006', '安太歲', 900),
]

print("初始化燈種數據...")
for lamp_id, lamp_name, price in lamp_types:
    lamp, created = LightingFeeTable.objects.get_or_create(
        Lamp_Type_ID=lamp_id,
        defaults={'Lamp_Type': lamp_name, 'Price': price}
    )
    if created:
        print(f'✓ 創建燈種: {lamp_name} (價格: {price})')
    else:
        print(f'✓ 燈種已存在: {lamp_name}')

# 創建測試點燈紀錄
print("\n創建測試數據...")
try:
    if Household_Information.objects.exists() and Member_Information.objects.exists():
        household = Household_Information.objects.first()
        member = Member_Information.objects.first()
        lamp = LightingFeeTable.objects.first()
        
        record = LightingRecordTable.objects.create(
            Lighting_Record_ID=str(uuid4()),
            Household_ID=household,
            Member_ID=member,
            Lamp_Type_ID=lamp,
            Year=2025,
            Lamp_Lighting_Date=date.today(),
            Amount=500,
            is_paid=False
        )
        print(f'✓ 創建測試點燈紀錄: {record.Lighting_Record_ID}')
except Exception as e:
    print(f'✗ 創建點燈紀錄失敗: {e}')

print(f'\n數據統計:')
print(f'  Household_Information: {Household_Information.objects.count()} 筆')
print(f'  Member_Information: {Member_Information.objects.count()} 筆')
print(f'  LightingFeeTable: {LightingFeeTable.objects.count()} 筆')
print(f'  LightingRecordTable: {LightingRecordTable.objects.count()} 筆')
