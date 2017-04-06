# contacts-api 

A simple flask-based RESTful API for contact management

## Installation & Starting Server

Something helpful goes here.

## Endpoints

### GET /api/v1/contacts

Gets a lsiting of all contacts. 
Optionally can filter by email:

```
GET /api/v1/contacts?email=example@email.com
```

### GET /api/v1/contacts/<contact_id>/

Returns a single contact by contact_id value

### POST /api/v1/contacts

Creates a new contact with data passed in.
first_name, last_name and email are required
address is optional

Example data - 

```json
{
    "first_name": "Jonny",
    "last_name": "Greenwood",
    "email": "jonny@ondes-martenot.co.uk",
    "address": "123 someplace rd, oxford uk"
}
```

### PUT /api/v1/contacts/<contact_id>/

Replaces data for a given existing contact_id.
All existing data is replaced, including optional fields not included. 

### DELETE /api/v1/contacts/<contact_id>/

Removes a contact given an existing contact_id.
