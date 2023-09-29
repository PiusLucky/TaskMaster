from flask import Blueprint
from app.controllers.task_tracker_controller import get_items

item_routes = Blueprint('item_routes', __name__)

@item_routes.route('/api/items', methods=['GET'])
def api_get_items():
    return get_items()