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
