from flask import Blueprint

health_check_route = Blueprint('health_check_route', __name__)

@health_check_route.route('/', methods=['GET'])
def health_check():
   return {
        "status": 200,
        "message": "Welcome to Task Master API v1 🚀",
        "ping": "2023-09-30T12:12:13.690Z"
    }
