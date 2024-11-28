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
def get_all_members():
    members = jackson_family.get_all_members()
    if members == []:
        return jsonify({"error": "there is not member"}), 404
    return jsonify(members),200
    
    

    # this is how you can use the Family datastructure by calling its methods
@app.route('/member/<int:member_id>', methods=['GET']) 
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}),400



@app.route('/member', methods=['POST'])
def add_member():
    body = request.json
    if not body or "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
        return jsonify({"error": "Missing required filds"}), 400
    
    
    added_member = jackson_family.add_member(body)
    return (added_member),200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    if success:
        return jsonify({"message": "Member deleted successfully","done":True}),200
    return jsonify({"error": "Member not found"}), 400


@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing request body"}), 400
    
    update_member = jackson_family.update_member(member_id, body)
    if update_member:
        return jsonify(update_member), 200
    return jsonify({"error": "Member not found"}), 400





       
        


    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
