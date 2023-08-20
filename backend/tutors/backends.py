from django.contrib.auth.backends import ModelBackend
from .models import TutorUser, ClientUser

class MultiUserModelBackend(ModelBackend):
    """Для расширения User модели и для возможности реализации авторизации для 2 моделей пользователей
       Сделан для тестеровании некоторых функции и не несет смысла для реального проекта
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = TutorUser.objects.get(email=email)
        except TutorUser.DoesNotExist:
            try:
                user = ClientUser.objects.get(email=email)
            except ClientUser.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None