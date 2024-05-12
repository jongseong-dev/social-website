from django.contrib.auth.models import User

from account.models import Profile


class EmailAuthBackend:
    """
    Email을 사용한 인증 백엔드
    """

    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication

    Args:
    backend: 사용자 인증에 사용된ㄴ 소셜 인증 백엔드
    user: user instance
    args: additional arguments
    kwargs: additional keyword arguments
    """
    Profile.objects.get_or_create(user=user)
