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

    products = Product.query.all()
    product_goals = []
    total_goal = 0

    for product in products:
        product_monthly_revenue = product.revenue_this_month()
        goal_percentage = product_monthly_revenue / product.monthly_goal

        if goal_percentage >= 1:
            goal_percentage = 1
        
        product_goal = {
            'name' : product.name, 
            'goal_percentage' :  goal_percentage * 100
        }

        product_goals.append(product_goal)

        total_goal += product.monthly_goal

    earnings_this_month = monthly_earnings[-1][2]
    monthly_goal_percentage = (earnings_this_month / total_goal) * 100

    if monthly_goal_percentage > 100:
        monthly_goal_percentage = 100

    monthly_earnings_array = []
    for earnings in monthly_earnings[-12:]:
        monthly_earnings_array.append(earnings[2])

    this_month = this_year = datetime.today().month
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months = months[this_month:] + months[:this_month]

    context = {
        'orders_today' : orders_today,
        'earnings_this_month' : earnings_this_month,
        'yearly_earnings' : yearly_earnings,
        'product_goals' : product_goals,
        'monthly_goal_percentage' : monthly_goal_percentage,
        'monthly_earnings_array' : monthly_earnings_array,
        'months' : months
    }

    return render_template('index.html', **context)

@main.route('/orders')
def orders():
    return render_template('tables.html')