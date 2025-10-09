from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
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

        print('Email: ', email)
        print('Password: ', password)
        print('Location: ', location)
        print('First Learn Date: ', first_learn_date)
        print('Fav Language: ', fav_language)
        print('About: ', about)
        print('Learn New Interest: ', learn_new_interest)
        print('Interest In Topics: ', interest_in_topics)

        return 'Form Submitted!'
    return render_template('form.html')