#!bin/python

import json

from flask import Flask, jsonify, abort

app = Flask(__name__)
BASE_URL = '/api/v1/contacts'
contacts = {'key': 'value'}

# routes
@app.route(BASE_URL, methods=['GET'])
def list_contacts():
    return jsonify(contacts)

@app.route(BASE_URL + '/<contact_id>', methods=['GET'])
def get_contact(contact_id):
    if contact_id in contacts:
        return jsonify(contacts)
    else:
        abort(404)

@app.route(BASE_URL, methods=['POST'])
def add_contact():
    # check auth TODO

    # validate data

    # create UUID

    # add data to list

    # return UUID

    pass

# error handlers (TODO)

if __name__=='__main__':
    app.run(debug=True)