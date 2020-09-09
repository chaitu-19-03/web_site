from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app1 import db, bcrypt
from app1.models import user, post
from app1.users.forms import (reg_form, login_form, update_form,
                                   request_reset_form, reset_password_form)
from app1.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)


@users.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = reg_form()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash('form.password.data')
        userx = user(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(userx)
        db.session.commit()
        flash(f'account created for {form.username.data}','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='register',form=form)

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    form = login_form()
    if form.validate_on_submit():
        user_x = user.query.filter_by(email=form.email.data).first()
        if user_x and (user_x.password==form.password.data):
            login_user(user_x,remember = form.remember.data)
            flash('Login successful... ', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else :
                return redirect(url_for('main.home'))

        else :
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',title='login',form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))



@users.route('/user/<string:username>')
def user_post(username):
    page = request.args.get('page',1,type=int)
    user_x = user.query.filter_by(username = username).first_or_404()
    posts = post.query.filter_by(author = user_x)\
    .order_by(post.date.desc())\
    .paginate(page = page,per_page = 3)

    return render_template('user_post.html',title = 'user Page',posts = posts,user=user_x)


@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    form = request_reset_form()
    if form.validate_on_submit():
        user_x = user.query.filter_by(email=form.email.data).first()
        send_rest_email(user_x)
        flash(f'email has been sent to {form.email.data}','success')
        return redirect(url_for('main.home'))
    return render_template('request_reset.html',title = 'reset request',form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])

def reset_token(token):
    if current_user.is_authenticated:
       return redirect(url_for('main.home'))
    user_x = user.verify_reset_token(token)
    if user_x is None :
        flash('this is invalid or expired token','success')
        return redirect(url_for('users.reset_request'))
    form = reset_password_form()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash('form.password.data')
        user_x.password = form.password.data
        db.session.commit()
        flash(f'password is changed ','success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',title = 'reset password',form=form)


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    image_file = url_for('static',filename='pics/'+current_user.image_file)
    form = update_form()
    if form.validate_on_submit():
        if form.pro_pic.data:
            picture_file = save_picture(form.pro_pic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
