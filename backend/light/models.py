import uuid
from django.db import models
from believer.models import Household_Information, Member_Information





class PrintStatus(models.TextChoices):
    NOT_PRINTED = 'not_printed', 'Not Printed'
    PRINTED = 'printed', 'Printed'


# ==========================================
# 費用表
# ==========================================

class LightingFeeTable(models.Model):

    Lamp_Type_ID = models.CharField(
        max_length=50,
        primary_key=True
    )

    Lamp_Type = models.CharField(
        max_length=100
    )

    Price = models.IntegerField()

    def __str__(self):
        return self.Lamp_Type


# ==========================================
# 點燈紀錄表
# ==========================================

class LightingRecordTable(models.Model):

    Lighting_Record_ID = models.CharField(
        max_length=50,
        primary_key=True
    )

    Household_ID = models.ForeignKey(
        Household_Information,
        on_delete=models.CASCADE
    )

    Member_ID = models.ForeignKey(
        Member_Information,
        on_delete=models.CASCADE
    )

    Lamp_Type_ID = models.ForeignKey(
        LightingFeeTable,
        on_delete=models.CASCADE
    )

    Year = models.IntegerField()

    Lamp_Lighting_Date = models.DateField()

    Record_Creation_Time = models.DateTimeField(
        auto_now_add=True
    )

    Record_Updated_Time = models.DateTimeField(
        auto_now=True
    )

    print_status = models.CharField(
        max_length=20,
        choices=PrintStatus.choices,
        default=PrintStatus.NOT_PRINTED
    )
    
    # 新增
    is_paid = models.BooleanField(
        default=False,
        verbose_name="是否已繳費"
    )

    payment_ref = models.ForeignKey(
        'LightingPaymentTable',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="關聯繳費紀錄"
    )

    # 新增: 點燈金額與備註
    Amount = models.IntegerField(
        default=0,
        verbose_name="點燈金額"
    )

    Notes = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="備註"
    )

    class Meta:
        unique_together = (
            'Member_ID',
            'Lamp_Type_ID',
            'Year'
        )

    def __str__(self):
        return self.Lighting_Record_ID
    


#==========================================
# 結算紀錄表
# ==========================================

class LightingPaymentTable(models.Model):
    Payment_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Household_ID = models.ForeignKey(
        Household_Information, 
        on_delete=models.CASCADE, 
        verbose_name="所屬住戶"
    )
    Payment_Time = models.DateTimeField(auto_now_add=True, verbose_name="繳費時間")
    GuangMing_Count = models.IntegerField(default=0, verbose_name="光明燈數量")
    TaiSui_Count = models.IntegerField(default=0, verbose_name="太歲燈數量")
    Total_Amount = models.IntegerField(default=0, verbose_name="總金額")

    class Meta:
        db_table = 'lighting_payment_table'