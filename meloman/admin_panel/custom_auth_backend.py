from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None

    def unauthorized(self, request, message=None):
        return HttpResponseRedirect(reverse_lazy('login'))
