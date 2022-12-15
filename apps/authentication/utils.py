from datetime import datetime

import jwt
from rest_framework_jwt.settings import api_settings


def jwt_encode_handler(payload):
    return jwt.encode(
        payload,
        api_settings.JWT_SECRET_KEY,
        api_settings.JWT_ALGORITHM
    ).decode('utf-8')


def jwt_decode_handler(token):
    return jwt.decode(
        token,
        api_settings.JWT_SECRET_KEY,
        algorithms=[api_settings.JWT_ALGORITHM]
    )


def jwt_payload_handler(user, time_token):
    return {
        'user_id': user.pk,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': time_token
    }


def jwt_get_user_id(payload):
    return payload.get('user_id')


def jwt_get_orig_iat(payload):
    return payload.get('orig_iat')
