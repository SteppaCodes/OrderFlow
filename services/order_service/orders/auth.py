from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class JWTAuth(JWTAuthentication):

    def get_user(self, validated_token):
        """
        Extract user info from token
        """
        try:
            user_id = validated_token.get('user_id')

            class TokenUser:
                def __init__(self, user_id):
                    self.id = user_id
                    self.is_authenticated = True
                
                def __str__(self):
                    return str(self.id)
            
            return TokenUser(user_id)
            
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')