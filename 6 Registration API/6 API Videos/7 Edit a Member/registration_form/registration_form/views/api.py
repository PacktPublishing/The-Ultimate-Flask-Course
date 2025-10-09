from datetime import datetime

from flask import Blueprint, jsonify, request

from registration_form.extensions import db
from registration_form.models import Member, Topic

api = Blueprint('api', __name__)

@api.route('/member', methods=['GET'])
def get_members():
    members = Member.query.all()

    return jsonify({'members' : [member.to_json() for member in members]})

@api.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get(member_id)

    return jsonify({'member' : member.to_json()})

@api.route('/member', methods=['POST'])
def create_member():
    member_req_data = request.get_json()

    member = Member(
        email = member_req_data.get('email'),
        password = member_req_data.get('password'),
        location = member_req_data.get('location'),
        first_learn_date = datetime.strptime(
            member_req_data.get('first_learn_date'), 
            '%Y-%m-%d'
        ),
        fav_language = member_req_data['fav_language'].get('id'),
        about = member_req_data.get('about'),
        learn_new_interest = member_req_data.get('learn_new_interest')
    )

    interest_in_topics = member_req_data.get('interest_in_topics')

    for member_topic in interest_in_topics:
        topic = Topic.query.get(member_topic['id'])
        member.interest_in_topics.append(topic)

    db.session.add(member)
    db.session.commit()

    return jsonify({'member' : member.to_json()})

@api.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    member_req_data = request.get_json()

    member = Member.query.get(member_id)
    member.email = member_req_data.get('email')
    if member_req_data.get('password'):
        member.password = member_req_data.get('password')
    member.location = member_req_data.get('location')
    member.first_learn_date = datetime.strptime(
        member_req_data.get('first_learn_date'), 
        '%Y-%m-%d'
    )
    member.fav_language = member_req_data['fav_language'].get('id')
    member.about = member_req_data.get('about')
    member.learn_new_interest = member_req_data.get('learn_new_interest')

    member.interest_in_topics[:] = []

    interest_in_topics = member_req_data.get('interest_in_topics')

    for member_topic in interest_in_topics:
        topic = Topic.query.get(member_topic['id'])
        member.interest_in_topics.append(topic)

    db.session.commit()

    return jsonify({'member' : member.to_json()}) 