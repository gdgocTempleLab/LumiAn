from django.db import models


class Donation_Record(models.Model):
	"""捐款紀錄（預設新表）"""

	Donation_ID = models.AutoField(primary_key=True)
	Member_ID = models.CharField(max_length=100, null=True, blank=True)
	Believer_Name = models.CharField(max_length=100)
	Gregorian_Birthday = models.DateField()
	Donation_Amount = models.DecimalField(max_digits=12, decimal_places=2)
	Donation_Date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		managed = False
		db_table = "Donation_Record_Table"

	def __str__(self):
		return f"{self.Donation_ID} - {self.Believer_Name}"
