"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if members == []:
        return jsonify({"msg":"The request body is empty"}), 404
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    members = jackson_family.get_member(id)
    if members == []:
        return jsonify({"msg":"The request body is empty"}), 404
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.json
    if not request_body:
        return jsonify({'msg': 'Bad Request'}), 400
    members = jackson_family.add_member(request_body)
    return (members)


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    delete_members = jackson_family.delete_member(id)

    return jsonify(delete_members), 200
# GET /members

# status_code: 200 if success. 400 if bad request (wrong info). 500 if the server encounters an error

# RESPONSE BODY (content-type: application/json):

# []  <!--- List of members -->

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
