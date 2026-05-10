from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from believer.models import Member_Information
from system.permissions import IsAdminRole

from .models import Donation_Record


def _get_payload_data(request):
	data = request.data.get("Data", {})
	return data if isinstance(data, dict) else {}


def _response_error(message, http_status=status.HTTP_400_BAD_REQUEST):
	return Response({"Status": "Error", "Message": message}, status=http_status)


def _serialize_donation(record):
	return {
		"Donation_ID": record.Donation_ID,
		"Member_ID": record.Member_ID,
		"Believer_Name": record.Believer_Name,
		"Gregorian_Birthday": record.Gregorian_Birthday,
		"Donation_Amount": record.Donation_Amount,
		"Donation_Date": record.Donation_Date,
	}


# DON-001-01: 檢查捐贈信息（名字 + 生日是否為既有信徒）
class DonationBelieverCheckView(APIView):
	permission_classes = [IsAuthenticated, IsAdminRole]

	def post(self, request):
		data = _get_payload_data(request)
		believer_name = data.get("Believer_Name")
		gregorian_birthday = data.get("Gregorian_Birthday")

		if not believer_name or not gregorian_birthday:
			return _response_error("Believer_Name and Gregorian_Birthday are required.")

		member = Member_Information.objects.filter(
			name=believer_name,
			Gregorian_Birthday=gregorian_birthday,
		).first()

		if not member:
			return Response(
				{
					"Status": "Success",
					"Message": "Believer not found.",
					"Data": {"Exists": False},
				},
				status=status.HTTP_200_OK,
			)

		return Response(
			{
				"Status": "Success",
				"Message": "Believer exists.",
				"Data": {
					"Exists": True,
					"Believer": {
						"Member_ID": member.Member_ID,
						"Believer_Name": member.name,
						"Gregorian_Birthday": member.Gregorian_Birthday,
						"Household_ID": member.Household_ID,
					},
				},
			},
			status=status.HTTP_200_OK,
		)


# DON-001-02: 新增捐贈紀錄
class DonationCreateView(APIView):
	permission_classes = [IsAuthenticated, IsAdminRole]

	def post(self, request):
		data = _get_payload_data(request)
		believer_name = data.get("Believer_Name")
		gregorian_birthday = data.get("Gregorian_Birthday")
		donation_amount = data.get("Donation_Amount")
		donation_date = data.get("Donation_Date")

		if not believer_name or not gregorian_birthday or donation_amount is None or not donation_date:
			return _response_error(
				"Believer_Name, Gregorian_Birthday, Donation_Amount, and Donation_Date are required."
			)

		member = Member_Information.objects.filter(
			name=believer_name,
			Gregorian_Birthday=gregorian_birthday,
		).first()

		member_id = member.Member_ID if member else None

		try:
			record = Donation_Record.objects.create(
				Member_ID=member_id,
				Believer_Name=believer_name,
				Gregorian_Birthday=gregorian_birthday,
				Donation_Amount=donation_amount,
				Donation_Date=donation_date,
			)
		except Exception as e:
			return _response_error(f"Error creating donation record: {str(e)}")

		return Response(
			{
				"Status": "Success",
				"Message": "Donation record created successfully.",
				"Data": {"Donation": _serialize_donation(record)},
			},
			status=status.HTTP_201_CREATED,
		)
