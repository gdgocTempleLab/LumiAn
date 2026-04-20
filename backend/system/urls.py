from django.urls import path
from .views import LoginView, TemplateAPIView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    
    # ==========================================
    # API Route Template
    # You can copy and paste the line below to route your new API.
    # Don't forget to import your new View class above!
    # ==========================================
    # path('your-endpoint/', TemplateAPIView.as_view(), name='your_endpoint_name'),
]
