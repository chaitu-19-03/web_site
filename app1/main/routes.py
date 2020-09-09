from flask import render_template, request, Blueprint
from app1.models import post
main = Blueprint('main',__name__)



@main.route('/')
def home():
    page = request.args.get('page',1,type=int)
    posts = post.query.order_by(post.date.desc()).paginate(page = page,per_page = 3)
    return render_template('home.html',title = 'Home Page',posts = posts)

@main.route('/about')
def about():
    return render_template('about.html',title = 'about title')
