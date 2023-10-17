from flask import Blueprint
from datetime import datetime

health_check_route = Blueprint('health_check_route', __name__)


@health_check_route.route('/', methods=['GET'])
def health_check():
    return {
        "status": 200,
        "message": "Welcome to Task Master API v1",
        "ping": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
