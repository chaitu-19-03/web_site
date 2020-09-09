from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app1 import db
from app1.models import post
from app1.posts.forms import post_form

posts = Blueprint('posts',__name__)


@posts.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = post_form()
    if form.validate_on_submit():
        post_x = post(title=form.title.data,content=form.content.data,author = current_user)
        db.session.add(post_x)
        db.session.commit()
        flash('ur post has been posted','success')
        return redirect(url_for('main.home'))
    return render_template('post.html',title='post',form = form,legend = 'Add post')

@posts.route('/post/<int:post_id>')
def post_up(post_id):
    post_x = post.query.get_or_404(post_id)
    return render_template('post_upa.html',title='post update',post_x = post_x)


@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_up(post_id):
    post_x = post.query.get_or_404(post_id)
    if post_x.author != current_user :
        abort(403)
    form =  post_form()
    if form.validate_on_submit():
        post_x.title = form.title.data
        post_x.content = form.content.data
        db.session.commit()
        flash('post has been updated','success')
        return redirect(url_for('posts.post_up',post_id = post_x.id))
    elif request.method =='GET' :
        form.title.data = post_x.title
        form.content.data = post_x.content
    return render_template('post.html',title='update post',form = form,
                    legend = 'udpate post')

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post_x = post.query.get_or_404(post_id)
    if post_x.author != current_user :
        abort(403)
    db.session.delete(post_x)
    db.session.commit()
    flash('post has been deleted','success')
    return redirect(url_for('main.home'))
