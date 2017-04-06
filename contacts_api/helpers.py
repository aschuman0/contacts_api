import uuid

from flask import abort, jsonify, make_response, request

def validate_contact(form_data, user):
    input_data = {}

    input_data['modified_by'] = user

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

def email_filter(email_arg, contacts):
    filtered = []
    if contacts:
        for contact in contacts:
            if contact[contact.keys()[0]]['email'] == email_arg:
                filtered.append(contact)
    if filtered:
        return filtered
    else:
        abort(404)

def authenticate(request):
    allowed_users = {
        'user1': 'password1',
        'user2': 'verysecret',
        'another_user': 'openplz'
    }
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password

        if username in allowed_users.keys():
            if allowed_users[username] == password:
                return username
        abort(401)
    else:
        abort(401)