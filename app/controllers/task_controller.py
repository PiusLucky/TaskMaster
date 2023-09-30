from flask import request
from app.models.task_model import TaskModel
from server import db
from app.validators.task import TaskForm
from app.handlers.index import success_response, error_response
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import cast
from sqlalchemy import or_
from math import ceil



def createTaskController():
    try:
        user_id = get_jwt_identity()
        # Parse JSON data from the request
        json_data = request.get_json()

        # Initialize the TaskForm with JSON data
        taskForm = TaskForm(data=json_data)

        if taskForm.validate():
            # Form is valid, process the data
            title = json_data["title"]
            description = json_data["description"]
            category = json_data["category"]
            priority = json_data["priority"]
            dueDate = json_data["dueDate"]

            # Create a new TaskModel instance
            new_task = TaskModel(
                user_id=user_id,
                title=title,
                description=description,
                category=category,
                priority=priority,
                dueDate=dueDate
            )

            # Add the task to the database session
            db.session.add(new_task)

            # Commit the changes to the database
            db.session.commit()

            # Return a success response with the created task data
            return success_response(new_task.as_dict())
    
        else:
            # Form is not valid, return validation errors
            return error_response(taskForm.errors, 400)
    except Exception as e:
        # Handle any exceptions that occur during processing or validation
         return error_response(f"Something went wrong ({str(e)})", 500)
    



def updateTaskController(task_id):
    try:
        # Query the task to be updated by its ID
        task = TaskModel.query.get(task_id)

        if task is None:
            return error_response('Task not found', 404)

        json_data = request.get_json()

        # Initialize the TaskForm with JSON data and bind it to the existing task
        taskForm = TaskForm(data=json_data, obj=task)

        if taskForm.validate():
            # Update the task attributes from the form data
            task.title = json_data["title"]
            task.description = json_data["description"]
            task.category = json_data["category"]
            task.priority = json_data["priority"]
            task.dueDate = json_data["dueDate"]

            # Commit the changes to the database
            db.session.commit()

            return success_response(task.as_dict(), message='Task updated successfully')
        else:
            return error_response(taskForm.errors, 400)
    except Exception as e:
        return error_response(f"Something went wrong ({str(e)})", 500)
    

def deleteTaskController(task_id):
    try:
        # Find the task by ID
        task = TaskModel.query.get(task_id)

        if not task:
            return error_response('Task not found', 404)

        # Delete the task
        db.session.delete(task)
        db.session.commit()

        return success_response(message='Task deleted successfully')
    except Exception as e:
        return error_response(f"Something went wrong ({str(e)})", 500)
    


def getAllTasksController():
    try:
        user_id = get_jwt_identity()  # Get the user's identity from the JWT token

        # Parse query parameters from the request URL
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search_query = request.args.get('search', '')

        # Retrieve filter parameters for each field
        title_filter = request.args.get('title')
        description_filter = request.args.get('description')
        category_filter = request.args.get('category')
        priority_filter = request.args.get('priority')
        dueDate_filter = request.args.get('dueDate')

        # Query tasks with pagination
        tasks_query = TaskModel.query.filter_by(user_id=user_id)

        # Apply search criteria
        if search_query:
            tasks_query = tasks_query.filter(or_(
                TaskModel.title.ilike(f"%{search_query}%"),
                TaskModel.description.ilike(f"%{search_query}%"),
                TaskModel.category.ilike(f"%{search_query}%"),
                TaskModel.priority.ilike(f"%{search_query}%")
            ))

        # Apply filter criteria for each field
        filter_queries = []
        if title_filter:
            filter_queries.append(TaskModel.title.ilike(f"%{title_filter}%"))
        if description_filter:
            filter_queries.append(TaskModel.description.ilike(f"%{description_filter}%"))
        if category_filter:
            filter_queries.append(TaskModel.category.ilike(f"%{category_filter}%"))
        if priority_filter:
            filter_queries.append(TaskModel.priority.ilike(f"%{priority_filter}%"))
        if dueDate_filter:
            filter_queries.append(cast(TaskModel.dueDate, db.String).ilike(f"%{dueDate_filter}%"))

        if filter_queries:
            tasks_query = tasks_query.filter(or_(*filter_queries))

        total_elements = tasks_query.count()
        total_pages = (total_elements + limit - 1) // limit

        tasks = tasks_query.limit(limit).offset((page - 1) * limit).all()

        # Convert tasks to a list of dictionaries
        tasks_list = [task.as_dict() for task in tasks]

        # Prepare response data with pagination information
        response_data = {
            'tasks': tasks_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_elements': total_elements,
                'total_pages': total_pages
            }
        }

        return success_response(response_data)
    except Exception as e:
        # Handle any exceptions that occur during processing or validation
        return error_response(f"Something went wrong ({str(e)})", 500)