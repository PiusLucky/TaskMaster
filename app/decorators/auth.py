from app.handlers.response import error_response
from functools import wraps
from app.models.backlisted_jwt_token_model import BlacklistedTokenModel
from flask_jwt_extended import get_jwt


def non_revoked_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            jti = get_jwt()["jti"]
            # Check if the token is blacklisted (discarded)
            if BlacklistedTokenModel.query.filter_by(jti=jti).first():
                return error_response('Token has been revoked', 401)

        except Exception as e:
            return error_response(f'Unable to check if token has been revoked {e}', 500)

        return func(*args, **kwargs)

    return decorated
