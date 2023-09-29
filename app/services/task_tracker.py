from flask import jsonify
from app import db
from app.models import task_tracker_model


def get_task(task_id):
    task = task_tracker_model.query.get(task_id)
    if task:
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description})
    return jsonify({'error': 'Task not found'}), 404


def delete_task(task_id):
    task = task_tracker_model.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

