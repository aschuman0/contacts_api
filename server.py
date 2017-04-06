import uuid

from flask import Flask, jsonify, abort, make_response, request

from contacts_api.helpers import validate_contact, email_filter, authenticate

app = Flask(__name__)
BASE_URL = '/api/v1/contacts'
CONTACTS = []

# error handlers
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'unauthorized'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

# routes
@app.route(BASE_URL, methods=['GET'])
def list_contacts():
    # TODO - filter by query string
    if request.args.get('email'):
        filtered = email_filter(request.args.get('email'), CONTACTS)
        return make_response(jsonify(filtered), 200)
    else:
        return jsonify(CONTACTS)

@app.route(BASE_URL + '/<contact_id>/', methods=['GET'])
def get_contact(contact_id):
    if CONTACTS:
        for contact in CONTACTS:
            if contact_id in contact.keys():
                return jsonify(contact)
        abort(404)
    else:
        abort(404)

@app.route(BASE_URL, methods=['POST'])
def add_contact():
    user = authenticate(request)
    input_data = validate_contact(request.form, user)
    new_uuid = uuid.uuid4()
    CONTACTS.append({str(new_uuid) : input_data})
    return make_response(jsonify({'contact_id': str(new_uuid)}))

@app.route(BASE_URL + '/<contact_id>/', methods=['PUT'])
def replace_contact(contact_id):
    user = authenticate(request)
    input_data = validate_contact(request.form, user)

    if CONTACTS:
        for contact in CONTACTS:
            if contact_id in contact.keys():
                contact[contact_id] = input_data
                return make_response(jsonify({'ok': input_data}), 200)
        abort(404)
    else:
        abort(404)

@app.route(BASE_URL + '/<contact_id>/', methods=['DELETE'])
def delete_contact(contact_id):
    authenticate(request)
    if CONTACTS:
        for contact in CONTACTS:
            if contact_id in contact.keys():
                CONTACTS.pop(CONTACTS.index(contact))
                return make_response(jsonify({'deleted': contact}), 200)
        abort(404)
    else:
        abort(404)

if __name__=='__main__':
    app.run(debug=True)