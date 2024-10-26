from datetime import datetime
import uuid
import jwt
from rest_framework_jwt.settings import api_settings


class JwtTokenGenerator:

    def get_token(self, user):
        payload = self.set_payload(user)
        return jwt.encode(
            payload,
            self.secret_key,
            api_settings.JWT_ALGORITHM
        ).decode('utf-8')

    def verify_token(self, token):
        self.payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[api_settings.JWT_ALGORITHM]
        )
        return self.payload

    def set_payload(self, user):
        self.payload = {
            'user_id':  user.pk,
            'username': user.username,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
            'jti': str(uuid.uuid4()),
            'iat': datetime.now().timestamp()
        }
        return self.payload

    @property
    def secret_key(self):
        return str(api_settings.JWT_SECRET_KEY)

    @property
    def user_id(self):
        return self.payload.get('user_id')

    @property
    def username(self):
        return self.payload.get('username')

    @property
    def exp(self):
        return self.payload.get('exp')

    @property
    def jti(self):
        return self.payload.get('jti')

    @property
    def iat(self):
        return self.payload.get('iat')
