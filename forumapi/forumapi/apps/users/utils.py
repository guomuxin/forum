from django.contrib.auth.backends import ModelBackend
from users.models import User
from django.db.models import Q


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'avatar': "",
        'nickname': user.nickname,
    }

class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username)|Q(email=username)|Q(wxchat=username))
        except User.DoesNotExist:
            user = None
        else:
            if isinstance(user,User) and user.check_password(password) and self.user_can_authenticate(user):
                return user