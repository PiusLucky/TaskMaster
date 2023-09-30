from flask import Blueprint
from app.controllers.task_controller import get_items
from app.utils.constants import API_VERSION

task_route = Blueprint('task_route', __name__)


@task_route.route(f'{API_VERSION}/tasks', methods=['GET'])
def api_get_items():
    return get_items()