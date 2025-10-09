from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required

from dashboard.models import Order, Product

main = Blueprint('main', __name__)

@main.route('/')
@login_required
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
    monthly_orders_array = []
    for earnings in monthly_earnings[-12:]:
        monthly_earnings_array.append(earnings[2])
        monthly_orders_array.append(earnings[3])

    this_month = this_year = datetime.today().month
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_12_months = months[this_month:] + months[:this_month]
    last_6_months = last_12_months[-6:]

    revenue_per_product = Order.revenue_per_product()
    total_revenue = 0

    product_labels = []
    for product in revenue_per_product:
        total_revenue += product[1]
        product_labels.append(product[0])

    revenue_per_product_pct = []
    for product in revenue_per_product:
        percentage = product[1] / total_revenue
        revenue_per_product_pct.append(percentage * 100)

    revenue_per_product_data = {
        'labels' : product_labels,
        'data' : revenue_per_product_pct
    }

    context = {
        'orders_today' : orders_today,
        'earnings_this_month' : earnings_this_month,
        'yearly_earnings' : yearly_earnings,
        'product_goals' : product_goals,
        'monthly_goal_percentage' : monthly_goal_percentage,
        'monthly_earnings_array' : monthly_earnings_array,
        'last_12_months' : last_12_months,
        'last_6_months' : last_6_months,
        'revenue_per_product_data' : revenue_per_product_data,
        'monthly_orders_array' : monthly_orders_array[-6:]
    }

    return render_template('index.html', **context)

@main.route('/orders')
@login_required
def orders():
    orders = Order.query.all()

    context = {
        'orders' : orders
    }

    return render_template('tables.html', **context)