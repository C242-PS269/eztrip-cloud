from flask import Blueprint, request, jsonify
from app.schemas import Item
from app.services import list_items, retrieve_item, add_item, modify_item, remove_item

blueprint = Blueprint("items", __name__)

@blueprint.route("/", methods=["GET"])
def read_root():
    return "Server is up and running!"

@blueprint.route("/items", methods=["GET"])
def get_items():
    return jsonify(list_items())

@blueprint.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = retrieve_item(item_id)
    return jsonify(item) if item else ("Item not found", 404)

@blueprint.route("/items", methods=["POST"])
def create_item():
    item_data = request.json
    item = Item(**item_data)
    item_id = add_item(item)
    return jsonify({"id": item_id}), 201

@blueprint.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item_data = request.json
    item = Item(**item_data)
    modify_item(item_id, item)
    return "", 204

@blueprint.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    remove_item(item_id)
    return "", 204
