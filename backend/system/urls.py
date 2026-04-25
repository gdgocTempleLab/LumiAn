from django.urls import path
from .views import LoginView, TemplateAPIView, AccountListView, CreateAccountView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('account/list/', AccountListView.as_view(), name='account_list'),
    path('account/create/', CreateAccountView.as_view(), name='create_account'),
    
    # ==========================================
    # API Route Template
    # You can copy and paste the line below to route your new API.
    # Don't forget to import your new View class above!
    # ==========================================
    # path('your-endpoint/', TemplateAPIView.as_view(), name='your_endpoint_name'),
]
