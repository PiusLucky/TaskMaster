from flask import Blueprint
from app.controllers.task_controller import createTaskController, updateTaskController, deleteTaskController, getAllTasksController
from app.utils.constants import API_VERSION
from flask_jwt_extended import jwt_required
from app.decorators.task import owner_permission_required

task_route = Blueprint('task_route', __name__)

RESOURCE_NAME = "task"


@task_route.route(f'{API_VERSION}/{RESOURCE_NAME}/tasks', methods=['GET'])
@jwt_required()
def getTasks():
    return getAllTasksController()

@task_route.route(f'{API_VERSION}/{RESOURCE_NAME}/tasks', methods=['POST'])
@jwt_required()
def create_task():
    return createTaskController()

@task_route.route(f'{API_VERSION}/{RESOURCE_NAME}/tasks/<uuid:task_id>', methods=['PUT'])
@jwt_required()
@owner_permission_required
def update_task(task_id):
    return updateTaskController(task_id)

@task_route.route(f'{API_VERSION}/{RESOURCE_NAME}/tasks/<uuid:task_id>', methods=['DELETE'])
@jwt_required()
@owner_permission_required
def delete_task(task_id):
    return deleteTaskController(task_id)