from django.urls import path
<<<<<<< HEAD
<<<<<<< HEAD
from .views import LoginView, TemplateAPIView, AccountListView, CreateAccountView, AccountDetailView, UpdateAccountView, UpdateProfileView, ChangePasswordView, AdminResetPasswordView
=======
from .views import LoginView, TemplateAPIView, AccountListView
>>>>>>> 09f9d84 (feat: implement authentication login and account listing API endpoints)
=======
from .views import LoginView, TemplateAPIView, AccountListView, CreateAccountView
>>>>>>> e050925 (feat: Finish user creating API)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('account/list/', AccountListView.as_view(), name='account_list'),
<<<<<<< HEAD
<<<<<<< HEAD
    path('account/create/', CreateAccountView.as_view(), name='create_account'),
    path('account/detail/', AccountDetailView.as_view(), name='account_detail'),
    path('account/update/', UpdateAccountView.as_view(), name='update_account'),
    path('account/reset-password/', AdminResetPasswordView.as_view(), name='admin_reset_password'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
=======
>>>>>>> 09f9d84 (feat: implement authentication login and account listing API endpoints)
=======
    path('account/create/', CreateAccountView.as_view(), name='create_account'),
>>>>>>> e050925 (feat: Finish user creating API)
    
    # ==========================================
    # API Route Template
    # You can copy and paste the line below to route your new API.
    # Don't forget to import your new View class above!
    # ==========================================
    # path('your-endpoint/', TemplateAPIView.as_view(), name='your_endpoint_name'),
]
