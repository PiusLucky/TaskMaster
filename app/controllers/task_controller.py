from flask import jsonify

def get_items():
    # Replace this with your actual logic to retrieve items from a database or another source.
    items = ["Item 1", "Item 2", "Item 3"]
    return jsonify({"items": items})