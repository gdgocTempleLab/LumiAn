from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

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
            # Generate Token via simplejwt RefreshToken
            refresh = RefreshToken.for_user(user)
            
            # --- Adding Role Information ---
            # You can customize this logic to pull the role from your user model.
            # Example: user.groups, user.is_staff, or a custom Profile model.
            role = "Admin" if user.is_superuser else "User"
            refresh['role'] = role # This puts the role into the access token payload

            access_token = str(refresh.access_token)

            return Response({
                "Status": "Success",
                "Data": {
                    "AccessToken": access_token
                }
            })
        else:
            return Response({
                "Status": "Error",
                "Message": "Invalid credentials."
            }, status=status.HTTP_401_UNAUTHORIZED)


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
