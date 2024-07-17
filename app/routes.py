from flask import Blueprint, request, jsonify, current_app
from app.models import get_form_collection, get_response_collection
from bson.objectid import ObjectId
import uuid

main = Blueprint('main', __name__)


# @main.route('/forms/create', methods=['POST'])
# def create_form():
#     data = request.get_json()
#     form_collection = get_form_collection()
#     result = form_collection.insert_one(data)
#     return jsonify({'_id': str(result.inserted_id)}), 201

@main.route('/form/create', methods=['POST'])
def create_form():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    form_id = str(uuid.uuid4())
    data['_id'] = form_id
    form_collection = current_app.db.forms
    print(form_collection)

    try:
        result = form_collection.insert_one(data)
        return jsonify({"message": "Form created", "form_id": form_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/forms/<id>', methods=['GET'])
def get_form(id):
    form_collection = get_form_collection()
    form = form_collection.find_one({'_id': ObjectId(id)})
    form['_id'] = str(form['_id'])
    return jsonify(form)


@main.route('/responses/<form_id>', methods=['POST'])
def submit_response(form_id):
    data = request.get_json()
    response_collection = get_response_collection()
    result = response_collection.insert_one({
        'form_id': ObjectId(form_id),
        'responses': data
    })
    return jsonify({'_id': str(result.inserted_id)}), 201


@main.route('/responses/<form_id>', methods=['GET'])
def get_responses(form_id):
    response_collection = get_response_collection()
    responses = list(response_collection.find({'form_id': ObjectId(form_id)}))
    for response in responses:
        response['_id'] = str(response['_id'])
        response['form_id'] = str(response['form_id'])
    return jsonify(responses)
