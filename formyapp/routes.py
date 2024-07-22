from flask import Blueprint, request, jsonify, current_app
from formyapp.models import get_form_collection, get_response_collection
from bson.objectid import ObjectId
import uuid
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

main = Blueprint('main', __name__)
bcrypt = Bcrypt()


# Register user
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    current_app.db.users.insert_one({'username': username, 'password': hashed_password})

    return jsonify({'message': 'User registered successfully'}), 201


# Login user
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = current_app.db.users.find_one({'username': username})
    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


# Secure route example
@main.route('/secure-data', methods=['GET'])
@jwt_required()
def secure_data():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Protecting a route with JWT
@main.route('/secure-endpoint', methods=['GET'])
@jwt_required()
def secure_endpoint():
    current_user = get_jwt_identity()
    return jsonify(message="This is a protected endpoint", user=current_user)


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
        print(f"Error creating form: {e}")
        return jsonify({'error': 'An error occurred'}), 500


@main.route('/formslist', methods=['GET'])
def get_forms():
    form_collection = current_app.db.forms
    forms = list(form_collection.find({}))
    for form in forms:
        form['_id'] = str(form['_id'])
    return jsonify(forms)


@main.route('/forms/<form_id>', methods=['GET'])
def get_form(form_id):
    try:
        form_collection = get_form_collection()
        # form = form_collection.find_one({'_id': ObjectId(form_id)})
        form = form_collection.find_one({'_id': form_id})
        if form:
            # form['_id'] = str(form['_id'])
            return jsonify(form), 200
        else:
            return jsonify({'error': 'Form not found'}), 404
    except Exception as e:
        print(f"Error retrieving form: {e}")
        return jsonify({'error': 'An error occurred'}), 500


@main.route('/responses/<form_id>', methods=['POST'])
def submit_response(form_id):
    data = request.get_json()
    response_collection = get_response_collection()
    try:
        result = response_collection.insert_one({
            'form_id': form_id,  # Store the form_id as UUID string
            'responses': data
        })
        return jsonify({'_id': str(result.inserted_id)}), 201
    except Exception as e:
        print(f"Error submitting response: {e}")
        return jsonify({'error': 'An error occurred'}), 500


@main.route('/responses/<form_id>', methods=['GET'])
def get_responses(form_id):
    response_collection = get_response_collection()
    form_collection = get_form_collection()
    try:
        responses = list(response_collection.find({'form_id': form_id}))  # Query by UUID string
        form = form_collection.find_one({'_id': form_id})  # Query by UUID string

        for response in responses:
            response['_id'] = str(response['_id'])
            response['form_id'] = str(response['form_id'])

        return jsonify(responses)
    except Exception as e:
        print(f"Error retrieving responses: {e}")
        return jsonify({'error': 'An error occurred'}), 500
