from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blogip import db
from blogip.models import Post,Comment
from blogip.posts.forms  import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, category=form.category.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:pitch>")
def post(pitch):
    post = Post.query.get_or_404(pitch)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:pitch>/update", methods=['GET', 'POST'])
@login_required
def update_post(pitch):
    post = Post.query.get_or_404(pitch)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category=form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', pitch=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data=post.category
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:pitch>/delete", methods=['POST'])
@login_required
def delete_post(pitch):
    post = Post.query.get_or_404(pitch)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted Successfuly!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/comment/<int:pitch>',methods = ['GET','POST'])
@login_required
def comment(pitch):
    blog=Post.query.get_or_404(pitch)
    form = CommentForm()
    allComments = Comment.query.filter_by(pitch = pitch).all()
    if form.validate_on_submit():
        postedComment = Comment(comment=form.comment.data,user_id = current_user.id, pitch = pitch)
        pitch = pitch
        db.session.add(postedComment)
        db.session.commit()
        flash('Your comment is posted')
        
        return redirect(url_for('posts.comment',pitch=pitch))

    return render_template("comment.html",blog=blog, title='React to blog!', form = form,allComments=allComments)


@posts.route('/blog/<int:pitch>', methods=['POST', 'GET'])

def blog(pitch):
    blog = Post.query.get_or_404(pitch)
    
    all_comments = Comment.query.filter_by(pitch=pitch).all()
    
    
    return render_template('post.html', blog=blog, all_comments=all_comments)