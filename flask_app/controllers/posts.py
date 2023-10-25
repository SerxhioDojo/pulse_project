from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment
import os
from flask import render_template, redirect, session, request, flash, jsonify
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_cors import CORS

CORS(app)
from werkzeug.utils import secure_filename


# Check if the format is right
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create Post Route
@app.route('/add/post')
def addPost():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        return render_template('addPost.html', loggedUser=loggedUser)
    return redirect('/')


# Create Post Form Control
@app.route('/create/post', methods=['POST'])
def createPost():
    if 'user_id' in session:
        if not Post.validate_post(request.form):
            return redirect(request.referrer)

        if not request.files['file']:
            flash('Post image is required!', 'postImage')
            return redirect(request.referrer)

        file = request.files['file']
        if not allowed_file(file.filename):
            flash('Image should be in png, jpg, jpeg format!', 'postImage')
            return redirect(request.referrer)

        if file and allowed_file(file.filename):
            filename1 = secure_filename(file.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        data = {
            'content': request.form['content'],
            'user_id': session['user_id'],
            'file': filename1
        }
        Post.save(data)
        return redirect('/dashboard')
    return redirect('/')


# Edit Post Form Route
@app.route('/edit/post/<int:id>')
def editPost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data)
        if loggedUser['id'] == post['user_id']:
            return render_template('editPost.html', loggedUser=loggedUser, post=post)
        return redirect('/dashboard')
    return redirect('/')


# Update Post Form
@app.route('/edit/post/<int:id>', methods=['POST'])
def updatePost(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data1)
        if loggedUser['id'] == post['user_id']:
            if not Post.validate_post(request.form):
                return redirect(request.referrer)
            data = {
                'content': request.form['content'],
                'post_id': id
            }
            Post.update(data)
            return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')


# View Post
@app.route('/post/<int:id>')
def viewPost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data)
        likes = Post.get_all_post_likes(data)
        comments = Comment.get_comments_by_post_id(data)
        return render_template('post.html', loggedUser=loggedUser, post=post, likes=likes,
                               liked_posts=User.get_user_liked_posts(data),
                               faved_posts=User.get_user_faved_posts(data), comments=comments)
    return redirect('/')


# Delete Post
@app.route('/delete/post/<int:id>')
def deletePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['isVerified'] == 0:
            return redirect('/verify/email')
        post = Post.get_post_by_id(data)
        if loggedUser['id'] == post['user_id']:
            Post.delete(data)
            return redirect(request.referrer)
        return redirect('/dashboard')
    return redirect('/')


# Like Post
@app.route('/like/post/<int:id>')
def likePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        post = Post.get_post_by_id(data)
        Post.like_post(data)
        return redirect(request.referrer)


# Unlike Post
@app.route('/unlike/post/<int:id>')
def unlikePost(id):
    if 'user_id' in session:
        if 'user_id' in session:
            data = {
                'user_id': session['user_id'],
                'post_id': id
            }
            loggedUser = User.get_user_by_id(data)
            post = Post.get_post_by_id(data)
            Post.unlike_post(data)
            return redirect(request.referrer)


# Fave Post
@app.route('/fave/post/<int:id>')
def favePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        post = Post.get_post_by_id(data)
        Post.fave_post(data)
        return redirect(request.referrer)


# Unfave Post
@app.route('/unfave/post/<int:id>')
def unfavePost(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'post_id': id
        }
        loggedUser = User.get_user_by_id(data)
        post = Post.get_post_by_id(data)
        Post.unfave_post(data)
        return redirect(request.referrer)


# Add Comment
@app.route('/add/comment/<int:id>', methods=['POST'])
def comment(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Comment.validate_comment(request.form):
        return redirect(request.referrer)

    data = {
        'user_id': session['user_id'],
        'post_id': id,
        'comment': request.form['comment']
    }
    loggedUser = User.get_user_by_id(data)
    post = Post.get_post_by_id(data)
    Comment.create(data)
    return redirect(request.referrer)


# Delete Comment
@app.route('/delete/comment/<int:id>')
def uncomment(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'comment_id': id
        }
        loggedUser = User.get_user_by_id(data)
        Comment.delete_comment(data)
        return redirect(request.referrer)
