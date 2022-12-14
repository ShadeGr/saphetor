from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
#from api.models import MyUser

from vcfapi.models import MyUser

def get_authorization_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    return auth

class BasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        
        if not auth or auth[0].lower() != "basic":
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Invalid basic header. No credentials provided.")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Invalid basic header. Credential string is not properly formatted")
        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, password):
        if password == 'test':
            user = MyUser()
            user.is_authenticated = True
            return user, None

        return None, None
    
    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        return MyUser()
