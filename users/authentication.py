from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    USER_MODEL = get_user_model()

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.USER_MODEL.objects.get(email=username)
            if user.check_password(password) and getattr(user, "is_active", True):
                return user
            return None
        except (self.USER_MODEL.DoesNotExist, self.USER_MODEL.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return self.USER_MODEL.objects.get(pk=user_id)
        except self.USER_MODEL.DoesNotExist:
            return None
