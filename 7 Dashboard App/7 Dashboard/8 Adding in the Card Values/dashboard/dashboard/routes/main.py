from datetime import datetime

from flask import Blueprint, render_template

from dashboard.models import Order, Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    beginning_of_day = datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    orders_today = Order.query.filter(Order.date > beginning_of_day).count()

    monthly_earnings = Order.get_monthly_earnings()

    yearly_earnings = 0
    this_year = datetime.today().year

    for month in monthly_earnings:
        if month[0] == this_year:
            yearly_earnings += month[2]

    context = {
        'orders_today' : orders_today,
        'earnings_this_month' : monthly_earnings[-1][2],
        'yearly_earnings' : yearly_earnings
    }

    return render_template('index.html', **context)

@main.route('/orders')
def orders():
    return render_template('tables.html')