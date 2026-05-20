from django.urls import path

from .views import (
    HouseholdCreateView,
    MemberCreateView,
    HouseholdUpdateView,
    HouseholdDetailView,
    MemberUpdateView,
    HouseholdDeleteView,
    MemberDeleteView,
    BelieverSearchView,
)

urlpatterns = [
    # BEL-001-1: 建立戶籍資料
    path("household/create/", HouseholdCreateView.as_view(), name="household_create"),
    # BEL-001-2: 新增戶員資料
    path("member/create/", MemberCreateView.as_view(), name="member_create"),
    # BEL-002-1: 更新戶籍基本資料
    path("household/update/", HouseholdUpdateView.as_view(), name="household_update"),
    # BEL-002-1: 取得戶籍詳細資料
    path("household/<str:household_id>/", HouseholdDetailView.as_view(), name="household_detail"),
    # BEL-002-2: 更新戶員資料
    path("member/update/", MemberUpdateView.as_view(), name="member_update"),
    # BEL-002-3: 刪除戶及資料
    path("household/delete/", HouseholdDeleteView.as_view(), name="household_delete"),
    # BEL-002-4: 刪除戶員資料
    path("member/delete/", MemberDeleteView.as_view(), name="member_delete"),
    # BEL-003: 查詢信徒資料
    path("search/", BelieverSearchView.as_view(), name="believer_search"),
]