from flask import current_app


def get_form_collection():
    return current_app.db['forms']


def get_response_collection():
    return current_app.db['responses']