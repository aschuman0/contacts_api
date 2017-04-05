#!bin/python

import json
import uuid
import time
import os

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)
BASE_URL = '/api/v1/contacts'
contacts = []

# routes
@app.route(BASE_URL, methods=['GET'])
@app.route(BASE_URL + '/', methods=['GET'])
def list_contacts():
    return jsonify(contacts)

@app.route(BASE_URL + '/<contact_id>', methods=['GET'])
@app.route(BASE_URL + '/<contact_id>/', methods=['GET'])
def get_contact(contact_id):
    if contacts:
        for contact in contacts:
            if contact_id in contact.keys():
                return jsonify(contact)
            else:
                return make_response(jsonify({'error': 'id not found'}), 404)
    else:
        return make_response(jsonify({'error': 'id not found'}), 404)

@app.route(BASE_URL, methods=['POST'])
@app.route(BASE_URL + '/', methods=['POST'])
def add_contact():
    
    # check auth TODO
    user = 'luv2auth'

    # validate data & build contact
    input_data = {}

    input_data['modifying_user'] = user

    if 'email' in request.form:
        input_data['email'] = request.form['email']
    else:
        return make_response(jsonify({'error': 'email required'}), 400)

    if 'first_name' in request.form:
        input_data['first_name'] = request.form['first_name']
    else:
        return make_response(jsonify({'error': 'first_name required'}), 400)

    if 'last_name' in request.form:
        input_data['last_name'] = request.form['last_name']
    else:
        return make_response(jsonify({'error': 'last_name required'}), 400)

    if 'address' in request.form:
        input_data['address'] = request.form['address']
    else:
        input_data['address'] = None

    # create UUID
    new_uuid = uuid.uuid4()

    contacts.append({str(new_uuid) : input_data})

    return make_response(jsonify({'contact_id': str(new_uuid)}))


# error handlers (TODO)

if __name__=='__main__':
    app.run(debug=True)