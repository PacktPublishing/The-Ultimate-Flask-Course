from flask import Blueprint, jsonify

from registration_form.models import Member

api = Blueprint('api', __name__)

@api.route('/member', methods=['GET'])
def get_members():
    members = Member.query.all()

    return jsonify({'members' : [member.to_json() for member in members]})