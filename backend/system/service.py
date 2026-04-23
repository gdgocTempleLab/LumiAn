# Here we put some utility functions.
# For example, JWT token operations can be defined here.

from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_token(user):
    """
    為指定的使用者產生 JWT (JSON Web Token)，
    並在 access token 的 payload 中加入角色 (role) 等自訂資訊。
    """
    # 產生 RefreshToken 與 AccessToken
    refresh = RefreshToken.for_user(user)
    
    # 取得使用者的角色，預設為 User
    role = getattr(user, 'role', 'User')
    
    # 將角色資訊加入 access token 的 payload 中
    refresh['role'] = role 
    
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }
