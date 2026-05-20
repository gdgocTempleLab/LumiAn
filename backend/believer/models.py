from django.db import models


class Household_Information(models.Model):
    """戶籍資訊表"""
    Household_ID = models.CharField(max_length=100, primary_key=True)
    Head_of_Household_ID = models.CharField(max_length=100, null=True, blank=True)
    Postal_code = models.IntegerField()
    Address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Household_Information_Table"

    def __str__(self):
        return f"{self.Household_ID}"


class Member_Information(models.Model):
    """信徒成員資訊表"""
    Member_ID = models.CharField(max_length=100, primary_key=True)
    Household = models.ForeignKey(
        Household_Information,
        on_delete=models.CASCADE,
        related_name='members',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    Lunar_Birthday = models.DateField()
    Gregorian_Birthday = models.DateField()
    isHeadOfHousehold = models.BooleanField(default=False)
    Profile_Creation_Time = models.DateTimeField(auto_now_add=True)
    Profile_Update_Time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Member_Information_Table"

    def __str__(self):
        return f"{self.Member_ID} - {self.name}"
