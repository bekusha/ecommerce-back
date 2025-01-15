from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class DeviceIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        device_id = request.headers.get('Device-ID')
        if not device_id:
            return None
        user, created = User.objects.get_or_create(username=device_id)
        if created:
            print(f"New user created: {user.username}")
        if not user.is_active:
            raise AuthenticationFailed("This device is not authorized.")
        print(f"Authenticated user: {user.username}")
        return (user, None)
