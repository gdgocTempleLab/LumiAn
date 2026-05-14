from django.urls import path
from .views import (
    CreateLightingRecordAPIView,
    SearchLightingRecordAPIView,
    UpdateLightingRecordAPIView,
    CalculateLightingFeeAPIView, 
    CreateLightingPaymentAPIView,
    MemberLightingStatusAPIView,
    DeleteLightingRecordAPIView,
    ExportLightingInventoryAPIView,
    LightStripPreviewAPIView,
    LightStripPrintConfirmAPIView
)

app_name = "light"


urlpatterns = [

    # 建立點燈紀錄
    path(
        "create/",
        CreateLightingRecordAPIView.as_view(),
        name="create_lighting_record"
    ),

    # 查詢點燈紀錄
    path(
        "search/",
        SearchLightingRecordAPIView.as_view(),
        name="search_lighting_record"
    ),
    
    # 查詢並顯示所有點燈清單 
    path(
        "member-status/<str:member_id>/", 
        MemberLightingStatusAPIView.as_view(), 
        name="member_lighting_status"
    ),

    # 編輯/更新點燈紀錄
    path(
        "update/<str:lighting_record_id>/",
        UpdateLightingRecordAPIView.as_view(),
        name="update_lighting_record"
    ),

    # 刪除/取消點燈紀錄
    path(
        "delete/<str:lighting_record_id>/", 
        DeleteLightingRecordAPIView.as_view(), 
        name="delete_lighting_record"
    ),

    path(
        "calculate-fee/",
        CalculateLightingFeeAPIView.as_view(),
        name="calculate_lighting_fee"
    ),

    path(
        "payment/create/",
        CreateLightingPaymentAPIView.as_view(),
        name="create_lighting_payment"
    ),
    # 匯出點燈清冊
    path(
        "export-inventory/", 
        ExportLightingInventoryAPIView.as_view(), 
        name="export_lighting_inventory"
    ),
    # 燈條列印預覽
    path(
        "print/preview/", 
        LightStripPreviewAPIView.as_view(), 
        name="light_strip_preview"),
    # 確認列印並更新狀態
    path("print/confirm/", 
    LightStripPrintConfirmAPIView.as_view(), 
    name="light_strip_print_confirm"),

]