from flask import render_template, redirect, session, request, jsonify
from flask_app import app
from flask_app.models.comments_model import Comment
from flask_app.models.posts_model import Post
from flask_app.models.users_model import User


@app.route('/posts/<int:id>/comments')
def new_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    post_id = {
        'id': id
    }

    logged_in_user = User.get_by_id(data)
    current_post = Post.show_post_and_creator(post_id)
    current_comments = Comment.get_all_post_comments(post_id)

    return render_template('postComment.html', logged_in_user=logged_in_user, current_post = current_post, current_comments=current_comments)
#create comment
@app.route('/posts/<int:id>/comments/create', methods = ['POST'])
def create_comment(id):
    is_valid, errors = Comment.validate_comment(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not is_valid:
       
        return jsonify({"success": False, "messages": errors})  # Send errors to frontend
    data = {
        "comment": request.form["comment"],
        "user_id": request.form["commenter"],
        "topic_id": request.form["post_comment"]
    }
    Comment.create_comment(data)
    return jsonify({"success": True, "messages": ["Comment added successfully!"]})


#removing comment
@app.route('/posts/<int:id>/comments/<int:id2>/delete', methods = ['POST'])
def remove_comment(id, id2):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id2
    }

    Comment.remove_comment(data)
    return redirect(f'/posts/{id}/comments')