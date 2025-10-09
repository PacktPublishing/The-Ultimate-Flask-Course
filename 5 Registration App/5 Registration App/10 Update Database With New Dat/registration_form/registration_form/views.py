from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from .extensions import db
from .models import Language, Topic, Member

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'], defaults={'member_id' : None})
@main.route('/<int:member_id>', methods=['GET', 'POST'])
def index(member_id):

    member = None
    if member_id:
        member = Member.query.get_or_404(member_id)
        
    if request.method == 'POST':
        # Gather Form Input
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        first_learn_date = request.form['first_learn_date']
        fav_language = request.form['fav_language']
        about = request.form['about']
        learn_new_interest = request.form['learn_new_interest']
        interest_in_topics = request.form.getlist('interest_in_topics')
    
        if member:
            member.email = email 

            if password:
                member.password = password

            member.location = location
            member.first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d')
            member.fav_language = fav_language
            member.about = about
            member.learn_new_interest = (
                True if learn_new_interest == 'yes' else False
            )

            member.interest_in_topics[:] = []
        
        else:
            member = Member(
                email = email,
                password = password,
                location = location,
                first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d'),
                fav_language = fav_language,
                about = about,
                learn_new_interest = (
                    True if learn_new_interest == 'yes' else False
                )
            )

            db.session.add(member)

        for topic_id in interest_in_topics:
            topic = Topic.query.get(int(topic_id))
            member.interest_in_topics.append(topic)

        db.session.commit()

        return redirect(url_for('main.index', member_id=member.id))

    languages = Language.query.all()
    topics = Topic.query.all()

    context = {
        'member_id' : member_id,
        'languages' : languages,
        'topics' : topics,
        'member' : member
    }

    return render_template('form.html', **context)