from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import (
    BelieverSearchView,
    HouseholdCreateView,
    HouseholdDeleteView,
    HouseholdUpdateView,
    MemberCreateView,
    MemberDeleteView,
    MemberUpdateView,
)


class BelieverApiTests(SimpleTestCase):
    # 這一整組測試，就像幫 API 做健康檢查。
    def setUp(self):
        # 先準備好假裝的工具和管理員角色，等一下每個測試都可以直接拿來用。
        self.factory = APIRequestFactory()
        self.admin_user = SimpleNamespace(is_authenticated=True, role="Admin")
        self.atomic_patcher = patch("believer.views.transaction.atomic")
        self.mock_atomic = self.atomic_patcher.start()
        self.addCleanup(self.atomic_patcher.stop)

        atomic_context = MagicMock()
        atomic_context.__enter__.return_value = None
        atomic_context.__exit__.return_value = False
        self.mock_atomic.return_value = atomic_context

    # 幫大家準備送出 POST 的小幫手。
    def _post(self, view, url_name, payload):
        request = self.factory.post(reverse(url_name), payload, format="json")
        force_authenticate(request, user=self.admin_user)
        return view.as_view()(request)

    # 幫大家準備送出 PUT 的小幫手。
    def _put(self, view, url_name, payload):
        request = self.factory.put(reverse(url_name), payload, format="json")
        force_authenticate(request, user=self.admin_user)
        return view.as_view()(request)

    # 幫大家準備送出 DELETE 的小幫手。
    def _delete(self, view, url_name, payload):
        request = self.factory.delete(reverse(url_name), payload, format="json")
        force_authenticate(request, user=self.admin_user)
        return view.as_view()(request)

    # 幫大家準備送出 GET 的小幫手。
    def _get(self, view, url_name, params=None):
        request = self.factory.get(reverse(url_name), params or {})
        force_authenticate(request, user=self.admin_user)
        return view.as_view()(request)

    @patch("believer.views.Household_Information.objects.create")
    @patch("believer.views.Household_Information.objects.filter")
    def test_bel_001_1_create_household(self, mock_filter, mock_create):
        # 這個測試在看：能不能先把一戶新家庭建立起來。
        mock_filter.return_value.exists.return_value = False
        mock_household = MagicMock()
        mock_household.Household_ID = "H001"
        mock_household.Head_of_Household_ID = None
        mock_household.Postal_code = 100
        mock_household.Address = "台北市中正區"
        mock_household.phone = "0911111111"
        mock_create.return_value = mock_household

        response = self._post(
            HouseholdCreateView,
            "household_create",
            {
                "Data": {
                    "Household_ID": "H001",
                    "Postal_code": 100,
                    "Address": "台北市中正區",
                    "phone": "0911111111",
                }
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["Status"], "Success")
        self.assertEqual(response.data["Data"]["Household"]["Household_ID"], "H001")

    @patch("believer.views.Household_Information.objects.filter")
    @patch("believer.views.Member_Information.objects.create")
    @patch("believer.views.Member_Information.objects.filter")
    def test_bel_001_2_create_member(self, mock_member_filter, mock_create, mock_household_filter):
        # 這個測試在看：能不能把一位家人加進某一戶裡。
        mock_household = MagicMock()
        mock_household.Household_ID = "H001"
        mock_household.Head_of_Household_ID = None
        mock_household.Postal_code = 100
        mock_household.Address = "台北市中正區"
        mock_household.phone = "0911111111"
        mock_household_filter.return_value.first.return_value = mock_household
        mock_member_filter.return_value.exists.return_value = False

        mock_member = MagicMock()
        mock_member.Member_ID = "M001"
        mock_member.Household_ID = "H001"
        mock_member.name = "王大明"
        mock_member.Lunar_Birthday = "1990-01-01"
        mock_member.Gregorian_Birthday = "1990-02-01"
        mock_member.isHeadOfHousehold = True
        mock_member.Profile_Creation_Time = "2026-05-10T00:00:00Z"
        mock_member.Profile_Update_Time = "2026-05-10T00:00:00Z"
        mock_create.return_value = mock_member

        response = self._post(
            MemberCreateView,
            "member_create",
            {
                "Data": {
                    "Member_ID": "M001",
                    "Household_ID": "H001",
                    "name": "王大明",
                    "Lunar_Birthday": "1990-01-01",
                    "Gregorian_Birthday": "1990-02-01",
                    "isHeadOfHousehold": True,
                }
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["Status"], "Success")
        self.assertEqual(response.data["Data"]["Member"]["Member_ID"], "M001")

    @patch("believer.views._serialize_household")
    @patch("believer.views.Household_Information.objects.filter")
    def test_bel_002_1_update_household(self, mock_filter, mock_serialize_household):
        # 這個測試在看：如果資料寫錯了，能不能改回來。
        mock_household = MagicMock()
        mock_household.Household_ID = "H001"
        mock_household.Head_of_Household_ID = "M001"
        mock_household.Postal_code = 100
        mock_household.Address = "舊地址"
        mock_household.phone = "0911111111"
        mock_filter.return_value.first.return_value = mock_household
        mock_serialize_household.return_value = {
            "Household_ID": "H001",
            "Head_of_Household_ID": "M001",
            "Postal_code": 100,
            "Address": "新地址",
            "phone": "0922222222",
            "Members": [],
        }

        response = self._put(
            HouseholdUpdateView,
            "household_update",
            {
                "Data": {
                    "Household_ID": "H001",
                    "Address": "新地址",
                    "phone": "0922222222",
                }
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Status"], "Success")
        mock_household.save.assert_called_once()

    @patch("believer.views.Household_Information.objects.get")
    @patch("believer.views.Member_Information.objects.filter")
    def test_bel_002_2_update_member(self, mock_member_filter, mock_household_get):
        # 這個測試在看：家人的名字或身分能不能更新。
        mock_member = MagicMock()
        mock_member.Member_ID = "M001"
        mock_member.Household_ID = "H001"
        mock_member.name = "王大明"
        mock_member.Lunar_Birthday = "1990-01-01"
        mock_member.Gregorian_Birthday = "1990-02-01"
        mock_member.isHeadOfHousehold = False
        mock_member_filter.return_value.first.return_value = mock_member

        mock_household = MagicMock()
        mock_household_get.return_value = mock_household

        response = self._put(
            MemberUpdateView,
            "member_update",
            {
                "Data": {
                    "Member_ID": "M001",
                    "Household_ID": "H001",
                    "name": "王更新",
                    "isHeadOfHousehold": True,
                }
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Status"], "Success")
        mock_member.save.assert_called_once()
        mock_household.save.assert_called_once()

    @patch("believer.views.Household_Information.objects.filter")
    @patch("believer.views.Member_Information.objects.filter")
    def test_bel_002_3_delete_household(self, mock_member_filter, mock_household_filter):
        # 這個測試在看：整個家庭一起搬走時，能不能連戶籍都刪掉。
        mock_household = MagicMock()
        mock_household_filter.return_value.first.return_value = mock_household
        mock_member_filter.return_value.delete.return_value = (1, {})

        response = self._delete(
            HouseholdDeleteView,
            "household_delete",
            {"Data": {"Household_ID": "H001"}},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Status"], "Success")
        mock_household.delete.assert_called_once()

    @patch("believer.views.Member_Information.objects.filter")
    def test_bel_002_4_delete_member(self, mock_filter):
        # 這個測試在看：只刪掉一位家人，其他人還在不在。
        mock_member = MagicMock()
        mock_filter.return_value.first.return_value = mock_member

        response = self._delete(
            MemberDeleteView,
            "member_delete",
            {"Data": {"Member_ID": "M001", "Household_ID": "H001"}},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Status"], "Success")
        mock_member.delete.assert_called_once()

    @patch("believer.views.Household_Information.objects.prefetch_related")
    @patch("believer.views.Member_Information.objects.filter")
    def test_bel_003_search(self, mock_member_filter, mock_prefetch):
        # 這個測試在看：能不能像找玩具一樣，把想要的家庭找出來。
        mock_member_qs = MagicMock()
        mock_member_qs.values_list.return_value.distinct.return_value = ["H001"]
        mock_member_filter.return_value = mock_member_qs

        mock_household = MagicMock()
        mock_household.Household_ID = "H001"
        mock_household.Head_of_Household_ID = "M001"
        mock_household.Postal_code = 100
        mock_household.Address = "台北市中正區"
        mock_household.phone = "0911111111"

        mock_household_qs = MagicMock()
        mock_prefetch.return_value.all.return_value = mock_household_qs
        mock_household_qs.filter.return_value = [mock_household]

        with patch(
            "believer.views._serialize_household",
            return_value={
                "Household_ID": "H001",
                "Head_of_Household_ID": "M001",
                "Postal_code": 100,
                "Address": "台北市中正區",
                "phone": "0911111111",
                "Members": [],
            },
        ):
            response = self._get(BelieverSearchView, "believer_search", {"member_name": "王"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Status"], "Success")
        self.assertEqual(len(response.data["Data"]["HouseholdList"]), 1)

    def test_routes_exist(self):
        # 這個測試在看：每個網址是不是都有接好。
        self.assertEqual(reverse("household_create"), "/api/bel/household/create/")
        self.assertEqual(reverse("member_create"), "/api/bel/member/create/")
        self.assertEqual(reverse("household_update"), "/api/bel/household/update/")
        self.assertEqual(reverse("member_update"), "/api/bel/member/update/")
        self.assertEqual(reverse("household_delete"), "/api/bel/household/delete/")
        self.assertEqual(reverse("member_delete"), "/api/bel/member/delete/")
        self.assertEqual(reverse("believer_search"), "/api/bel/search/")