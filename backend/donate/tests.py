from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import DonationBelieverCheckView, DonationCreateView


class DonateApiTests(SimpleTestCase):
	# 這一組測試會確認捐款 API 的基本行為都正確。
	def setUp(self):
		self.factory = APIRequestFactory()
		self.admin_user = SimpleNamespace(is_authenticated=True, role="Admin")

	def _post(self, view, url_name, payload):
		request = self.factory.post(reverse(url_name), payload, format="json")
		force_authenticate(request, user=self.admin_user)
		return view.as_view()(request)

	@patch("donate.views.Member_Information.objects.filter")
	def test_don_001_01_check_believer_exists(self, mock_member_filter):
		# 這個測試在看：輸入名字和生日時，能不能找到既有信徒。
		mock_member = MagicMock()
		mock_member.Member_ID = "M001"
		mock_member.name = "王小明"
		mock_member.Gregorian_Birthday = "1990-01-01"
		mock_member.Household_ID = "H001"
		mock_member_filter.return_value.first.return_value = mock_member

		response = self._post(
			DonationBelieverCheckView,
			"donation_check",
			{
				"Data": {
					"Believer_Name": "王小明",
					"Gregorian_Birthday": "1990-01-01",
				}
			},
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["Status"], "Success")
		self.assertEqual(response.data["Data"]["Exists"], True)
		self.assertEqual(response.data["Data"]["Believer"]["Member_ID"], "M001")

	def test_don_001_01_check_missing_args(self):
		# 這個測試在看：欄位不完整時，會不會回傳錯誤訊息。
		response = self._post(
			DonationBelieverCheckView,
			"donation_check",
			{"Data": {"Believer_Name": "王小明"}},
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data["Status"], "Error")

	@patch("donate.views.Donation_Record.objects.create")
	@patch("donate.views.Member_Information.objects.filter")
	def test_don_001_02_create_donation_success(self, mock_member_filter, mock_create):
		# 這個測試在看：新增捐款時，能不能正確寫入一筆紀錄。
		mock_member = MagicMock()
		mock_member.Member_ID = "M001"
		mock_member_filter.return_value.first.return_value = mock_member

		mock_record = MagicMock()
		mock_record.Donation_ID = 1
		mock_record.Member_ID = "M001"
		mock_record.Believer_Name = "王小明"
		mock_record.Gregorian_Birthday = "1990-01-01"
		mock_record.Donation_Amount = "1200.00"
		mock_record.Donation_Date = "2026-05-10"
		mock_create.return_value = mock_record

		response = self._post(
			DonationCreateView,
			"donation_create",
			{
				"Data": {
					"Believer_Name": "王小明",
					"Gregorian_Birthday": "1990-01-01",
					"Donation_Amount": "1200.00",
					"Donation_Date": "2026-05-10",
				}
			},
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["Status"], "Success")
		self.assertEqual(response.data["Data"]["Donation"]["Donation_ID"], 1)

	def test_don_001_02_create_donation_missing_args(self):
		# 這個測試在看：缺少金額或日期時，不應該建立捐款。
		response = self._post(
			DonationCreateView,
			"donation_create",
			{
				"Data": {
					"Believer_Name": "王小明",
					"Gregorian_Birthday": "1990-01-01",
				}
			},
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data["Status"], "Error")

	def test_routes_exist(self):
		# 這個測試在看：donate 的兩個網址是不是都有接好。
		self.assertEqual(reverse("donation_check"), "/api/don/check/")
		self.assertEqual(reverse("donation_create"), "/api/don/create/")
