from datetime import datetime

from werkzeug.security import generate_password_hash

from .extensions import db 

member_topic_table = db.Table('member_topic',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True)
)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(50))
    location = db.Column(db.String(30))
    first_learn_date = db.Column(db.DateTime)
    fav_language = db.Column(db.ForeignKey('language.id'))
    about = db.Column(db.Text)
    learn_new_interest = db.Column(db.Boolean)

    interest_in_topics = db.relationship(
        'Topic',
        secondary=member_topic_table,
        lazy=True,
        backref=db.backref('topic', lazy=True)
    )

    @property
    def password(self):
        raise AttributeError('Cannot view password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_json(self):
        topics = []
        for topic in self.interest_in_topics:
            topics.append({'id': topic.id, 'name' : topic.name})

        fav_language = Language.query.get(self.fav_language)

        language_json = {
            'id' : fav_language.id,
            'name' : fav_language.name
        }

        member_json = {
            'id' : self.id,
            'email' : self.email,
            'location' : self.location,
            'first_learn_date' : datetime.strftime(self.first_learn_date, '%Y-%m-%d'),
            'fav_language' : language_json,
            'about' : self.about,
            'learn_new_interest' : self.learn_new_interest,
            'interest_in_topics' : topics
        }

        return member_json

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))