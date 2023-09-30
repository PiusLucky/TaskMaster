from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.task_model import TaskModel
from app.handlers.response import error_response

def owner_permission_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # Get the user_id from the JWT token
        user_id = get_jwt_identity()

        # Get the task_id from the route parameter
        task_id = kwargs.get('task_id')

        # Query the task to be updated by its ID
        task = TaskModel.query.get(task_id)

        if task is None:
            return error_response('Task not found', 404)

        # Check if the user is the owner of the task
        if str(task.user_id) != str(user_id):
            return error_response('You do not have permission to update this task', 403)
        
        kwargs['task_id'] = task_id
        return func(*args, **kwargs)

    return decorated