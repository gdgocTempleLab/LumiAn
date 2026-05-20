from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from system.permissions import IsAdminRole
from .models import Household_Information, Member_Information


def _get_payload_data(request):
    """獲取請求 body 中的 Data 欄位"""
    data = request.data.get("Data", {})
    return data if isinstance(data, dict) else {}


def _response_error(message, http_status=status.HTTP_400_BAD_REQUEST):
    """回傳錯誤訊息"""
    return Response(
        {"Status": "Error", "Message": message},
        status=http_status,
    )


def _serialize_member(member):
    """序列化單位成員"""
    return {
        "Member_ID": member.Member_ID,
        "Household_ID": member.Household.Household_ID if member.Household else None,
        "name": member.name,
        "Lunar_Birthday": member.Lunar_Birthday,
        "Gregorian_Birthday": member.Gregorian_Birthday,
        "isHeadOfHousehold": member.isHeadOfHousehold,
        "Profile_Creation_Time": member.Profile_Creation_Time,
        "Profile_Update_Time": member.Profile_Update_Time,
    }


def _serialize_household(household, include_members=True):
    """序列化戶籍資訊"""
    data = {
        "Household_ID": household.Household_ID,
        "Head_of_Household_ID": household.Head_of_Household_ID,
        "Postal_code": household.Postal_code,
        "Address": household.Address,
        "phone": household.phone,
        "mobile": household.mobile,
    }

    if include_members:
        members = household.members.all().order_by("Member_ID")
        data["Members"] = [_serialize_member(m) for m in members]

    return data


# BEL-001-1: 建立信徒資料-戶籍資料
class HouseholdCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        data = _get_payload_data(request)
        household_id = data.get("Household_ID")
        postal_code = data.get("Postal_code")
        address = data.get("Address")
        phone = data.get("phone")
        mobile = data.get("mobile", "")

        if not all([household_id, postal_code, address, phone]):
            return _response_error(
                "Household_ID, Postal_code, Address, and phone are required."
            )

        if Household_Information.objects.filter(Household_ID=household_id).exists():
            return _response_error("Household already exists.")

        try:
            household = Household_Information.objects.create(
                Household_ID=household_id,
                Postal_code=postal_code,
                Address=address,
                phone=phone,
                mobile=mobile,
            )

            return Response(
                {
                    "Status": "Success",
                    "Message": "Household created successfully.",
                    "Data": {"Household": _serialize_household(household, include_members=False)},
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return _response_error(f"Error creating household: {str(e)}")


# BEL-001-2: 建立信徒資料-新增護員資料
class MemberCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        data = _get_payload_data(request)
        member_id = data.get("Member_ID")
        household_id = data.get("Household_ID")
        name = data.get("name")
        lunar_birthday = data.get("Lunar_Birthday")
        gregorian_birthday = data.get("Gregorian_Birthday")
        is_head = bool(data.get("isHeadOfHousehold", False))

        if not all([member_id, household_id, name, lunar_birthday, gregorian_birthday]):
            return _response_error(
                "Member_ID, Household_ID, name, Lunar_Birthday, and Gregorian_Birthday are required."
            )

        household = Household_Information.objects.filter(
            Household_ID=household_id
        ).first()
        if not household:
            return _response_error("Household not found.", status.HTTP_404_NOT_FOUND)

        if Member_Information.objects.filter(Member_ID=member_id).exists():
            return _response_error("Member already exists.")

        try:
            with transaction.atomic():
                # 如果是戶長，清除該戶之前的戶長標籤
                if is_head:
                    Member_Information.objects.filter(
                        Household=household, isHeadOfHousehold=True
                    ).update(isHeadOfHousehold=False)

                member = Member_Information.objects.create(
                    Member_ID=member_id,
                    Household=household,
                    name=name,
                    Lunar_Birthday=lunar_birthday,
                    Gregorian_Birthday=gregorian_birthday,
                    isHeadOfHousehold=is_head,
                )

                # 更新戶籍的戶長 ID
                if is_head:
                    household.Head_of_Household_ID = member_id
                    household.save()

            return Response(
                {
                    "Status": "Success",
                    "Message": "Member created successfully.",
                    "Data": {"Member": _serialize_member(member)},
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return _response_error(f"Error creating member: {str(e)}")


# BEL-002-1: 編輯信徒資料-更新戶籍基本資料
class HouseholdUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def put(self, request):
        data = _get_payload_data(request)
        household_id = data.get("Household_ID")

        if not household_id:
            return _response_error("Household_ID is required.")

        household = Household_Information.objects.filter(
            Household_ID=household_id
        ).first()
        if not household:
            return _response_error("Household not found.", status.HTTP_404_NOT_FOUND)

        updated = False
        for field, source_key in [
            ("Postal_code", "Postal_code"),
            ("Address", "Address"),
            ("phone", "phone"),
            ("mobile", "mobile"),
        ]:
            if source_key in data:
                setattr(household, field, data.get(source_key))
                updated = True

        if not updated:
            return _response_error("No update fields provided.")

        household.save()

        return Response(
            {
                "Status": "Success",
                "Message": "Household updated successfully.",
                "Data": {"Household": _serialize_household(household)},
            },
            status=status.HTTP_200_OK,
        )


# BEL-002-1: 取得戶籍詳細資料
class HouseholdDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, household_id):
        household = Household_Information.objects.prefetch_related("members").filter(
            Household_ID=household_id
        ).first()
        if not household:
            return _response_error("Household not found.", status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "Status": "Success",
                "Data": {"Household": _serialize_household(household)},
            },
            status=status.HTTP_200_OK,
        )


# BEL-002-2: 編輯信徒資料-更新戶員資料
class MemberUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def put(self, request):
        data = _get_payload_data(request)
        member_id = data.get("Member_ID")
        household_id = data.get("Household_ID")

        if not member_id or not household_id:
            return _response_error("Member_ID and Household_ID are required.")

        household = Household_Information.objects.filter(
            Household_ID=household_id
        ).first()
        if not household:
            return _response_error("Household not found.", status.HTTP_404_NOT_FOUND)

        member = Member_Information.objects.filter(
            Member_ID=member_id, Household=household
        ).first()
        if not member:
            return _response_error("Member not found.", status.HTTP_404_NOT_FOUND)

        updated = False
        for field, source_key in [
            ("name", "name"),
            ("Lunar_Birthday", "Lunar_Birthday"),
            ("Gregorian_Birthday", "Gregorian_Birthday"),
        ]:
            if source_key in data:
                setattr(member, field, data.get(source_key))
                updated = True

        # 處理是否為戶長的更新
        if "isHeadOfHousehold" in data:
            is_head = bool(data.get("isHeadOfHousehold"))
            if is_head and not member.isHeadOfHousehold:
                # 清除其他戶員的戶長標籤
                Member_Information.objects.filter(
                    Household=household, isHeadOfHousehold=True
                ).exclude(Member_ID=member_id).update(isHeadOfHousehold=False)
                
                # 更新戶籍的戶長 ID
                household.Head_of_Household_ID = member_id
                household.save()

            member.isHeadOfHousehold = is_head
            updated = True

        if not updated:
            return _response_error("No update fields provided.")

        member.save()

        return Response(
            {
                "Status": "Success",
                "Message": "Member updated successfully.",
                "Data": {"Member": _serialize_member(member)},
            },
            status=status.HTTP_200_OK,
        )


# BEL-002-3: 編輯信徒資料-刪除戶及資料
class HouseholdDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def delete(self, request):
        data = _get_payload_data(request)
        household_id = data.get("Household_ID")

        if not household_id:
            return _response_error("Household_ID is required.")

        household = Household_Information.objects.filter(
            Household_ID=household_id
        ).first()
        if not household:
            return _response_error("Household not found.", status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                # 刪除該戶的所有成員
                Member_Information.objects.filter(Household=household).delete()
                # 刪除該戶
                household.delete()

            return Response(
                {
                    "Status": "Success",
                    "Message": "Household and all members deleted successfully.",
                    "Data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return _response_error(f"Error deleting household: {str(e)}")


# BEL-002-4: 編輯信徒資料-刪除戶員資料
class MemberDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def delete(self, request):
        data = _get_payload_data(request)
        member_id = data.get("Member_ID")
        household_id = data.get("Household_ID")

        if not member_id or not household_id:
            return _response_error("Member_ID and Household_ID are required.")

        household = Household_Information.objects.filter(
            Household_ID=household_id
        ).first()
        if not household:
            return _response_error("Household not found.", status.HTTP_404_NOT_FOUND)

        member = Member_Information.objects.filter(
            Member_ID=member_id, Household=household
        ).first()
        if not member:
            return _response_error("Member not found.", status.HTTP_404_NOT_FOUND)

        try:
            member.delete()
            return Response(
                {
                    "Status": "Success",
                    "Message": "Member deleted successfully.",
                    "Data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return _response_error(f"Error deleting member: {str(e)}")


# BEL-003: 查詢信徒資料
class BelieverSearchView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        search_method = request.query_params.get("searchMethod", "").strip()
        search_text = request.query_params.get("searchText", "").strip()

        households = Household_Information.objects.prefetch_related(
            "members"
        ).all()

        # 按市話篩選
        if search_method == "phone" and search_text:
            households = households.filter(phone__icontains=search_text)

        # 按手機篩選 - 從成員表中查詢
        elif search_method == "mobile" and search_text:
            households = households.filter(mobile__icontains=search_text)

        # 按戶長名稱篩選
        elif search_method == "name" and search_text:
            head_households = Member_Information.objects.filter(
                name__icontains=search_text,
                isHeadOfHousehold=True,
            ).values_list("Household__Household_ID", flat=True).distinct()
            households = households.filter(
                Household_ID__in=head_households,
            )

        household_list = [_serialize_household(h) for h in households]

        return Response(
            {
                "Status": "Success",
                "Data": {"HouseholdList": household_list},
            },
            status=status.HTTP_200_OK,
        )
