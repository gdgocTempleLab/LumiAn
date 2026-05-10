from django.urls import path

from .views import DonationBelieverCheckView, DonationCreateView

urlpatterns = [
    # DON-001-01: 檢查捐贈信息
    path("check/", DonationBelieverCheckView.as_view(), name="donation_check"),
    # DON-001-02: 新增捐贈紀錄
    path("create/", DonationCreateView.as_view(), name="donation_create"),
]
