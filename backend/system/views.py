from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from .service import generate_jwt_token

User = get_user_model()

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminRole

class LoginView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = []
    
    def post(self, request):
        data = request.data.get("Data", {})
        username = data.get("Account")
        password = data.get("Password")

        if not username or not password:
            return Response({
                "Status": "Error",
                "Message": "Account and Password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using Django's built-in backend
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate Token via service
            token_data = generate_jwt_token(user)

            return Response({
                "Status": "Success",
                "Data": {
                    "AccessToken": token_data["access_token"]
                }
            })
        else:
            return Response({
                "Status": "Error",
                "Message": "Invalid credentials."
            }, status=status.HTTP_401_UNAUTHORIZED)

class AccountListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    def get(self, request):
        users = User.objects.all()
        account_list = []
        for user in users:
            account_list.append({
                "Id": user.user_id,
                "Account": user.account,
                "Role": user.role,
                "Email": user.email,
                "Account_Status": user.Account_Status,
                "Account_Creation_Time": user.Account_Creation_Time,
                "Account_Update_Time": user.Account_Update_Time
            })

        return Response({
            "Status": "Success",
            "Data": {
                "AccountList": account_list
            }
        }, status=status.HTTP_200_OK)


class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    def post(self, request):
        data = request.data.get("Data", {})
        account = data.get("Account")
        password = data.get("Password")
        role = data.get("Role")
        email = data.get("Email")
        account_status = data.get("Account_Status")
        
        if not account or not password or not role or not email or not account_status:
            return Response({
                "Status": "Error",
                "Message": "Missing arguments."
            }, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(account=account).exists():
            return Response({
                "Status": "Error",
                "Message": "Account already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(account=account, password=password, role=role, email=email, Account_Status=account_status)
        return Response({
            "Status": "Success",
            "Message": "Account created successfully."
        }, status=status.HTTP_201_CREATED)


# ==========================================
# API View Template
# You can copy and paste the class below to quickly create new APIs.
# ==========================================
class TemplateAPIView(APIView):
    """
    Template for creating a new API endpoint.
    """
    # Define permission classes if needed.
    # Example: permission_classes = [IsAuthenticated]
    # (Requires: from rest_framework.permissions import IsAuthenticated)
    permission_classes = []

    def get(self, request):
        """
        Handle GET requests.
        """
        # Example: Retrieve query parameters (e.g., /api/sys/endpoint/?name=test)
        # name = request.query_params.get('name')

        return Response({
            "Status": "Success",
            "Message": "GET request successful",
            "Data": {}
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST requests.
        """
        # Example: Retrieve JSON body data
        # data = request.data.get('Data', {})
        
        # Example: Basic validation
        # if not data:
        #     return Response({
        #         "Status": "Error",
        #         "Message": "Missing Data"
        #     }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "Status": "Success",
            "Message": "POST request successful",
            "Data": {}
        }, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        Handle PUT requests.
        """
        # data = request.data
        return Response({
            "Status": "Success",
            "Message": "PUT request successful",
            "Data": {}
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Handle DELETE requests.
        """
        return Response({
            "Status": "Success",
            "Message": "DELETE request successful",
            "Data": {}
        }, status=status.HTTP_200_OK)
