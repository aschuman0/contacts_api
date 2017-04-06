#!bin/python

import json
import uuid
import time
import os

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)
BASE_URL = '/api/v1/contacts'
contacts = []

def validate_contact(form_data, user):
    input_data = {}

    input_data['modifying_user'] = user

    if 'email' in request.form:
        input_data['email'] = form_data['email']
    else:
        abort(400)

    if 'first_name' in request.form:
        input_data['first_name'] = form_data['first_name']
    else:
        abort(400)

    if 'last_name' in request.form:
        input_data['last_name'] = form_data['last_name']
    else:
        abort(400)

    if 'address' in request.form:
        input_data['address'] = form_data['address']
    else:
        input_data['address'] = None

    return input_data

# error handlers
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

# routes
@app.route(BASE_URL, methods=['GET'])
def list_contacts():
    # TODO - filter by query string

    return jsonify(contacts)

@app.route(BASE_URL + '/<contact_id>/', methods=['GET'])
def get_contact(contact_id):
    if contacts:
        for contact in contacts:
            if contact_id in contact.keys():
                return jsonify(contact)
        abort(404)
    else:
        abort(404)

@app.route(BASE_URL, methods=['POST'])
def add_contact():
    
    # check auth TODO
    user = 'luv2add'

    # validate data & build contact
    input_data = validate_contact(request.form, user)

    # create UUID
    new_uuid = uuid.uuid4()

    contacts.append({str(new_uuid) : input_data})

    return make_response(jsonify({'contact_id': str(new_uuid)}))

@app.route(BASE_URL + '/<contact_id>/', methods=['PUT'])
def replace_contact(contact_id):
    
    # check auth TODO
    user = 'luv2change'

    input_data = validate_contact(request.form, user)

    if contacts:
        for contact in contacts:
            if contact_id in contact.keys():
                contact[contact_id] = input_data
                return make_response(jsonify({'ok': input_data}), 200)
        abort(404)
    else:
        abort(404)

@app.route(BASE_URL + '/<contact_id>/', methods=['DELETE'])
def delete_contact(contact_id):
    if contacts:
        for contact in contacts:
            if contact_id in contact.keys():
                # idx = contacts.index(contact)
                contacts.pop(contacts.index(contact))
                return make_response(jsonify({'deleted': contact}), 200)
        abort(404)
    else:
        abort(404)

if __name__=='__main__':
    app.run(debug=True)