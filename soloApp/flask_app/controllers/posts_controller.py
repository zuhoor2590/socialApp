from flask import render_template, redirect, session, request,jsonify, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.posts_model import Post


#route for showing all posts
@app.route('/posts')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    data = {
        'user_id': session['user_id']
    }

    logged_in_user = User.get_by_id(user_data)
    posts = Post.get_all_posts()
    post_adds = Post.get_all_post_adds(data)
    # print(post_adds)

    return render_template('allPosts.html', logged_in_user = logged_in_user, posts = posts, post_adds = post_adds)

#route for new post
@app.route('/posts/new')
def new_post():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    logged_in_user = User.get_by_id(data)
    return render_template('newPost.html', logged_in_user = logged_in_user)

@app.route('/posts/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "User not logged in"}), 403
    # Validate post data
    is_valid, errors = Post.validate_post(request.form)
    if not is_valid:
        return jsonify({"success": False, "messages": errors}) #400  # Send errors to frontend

    data = {
        "topic": request.form["topic"],
        "subtopic": request.form["subtopic"],
        "description": request.form["description"],
        "user_id": request.form["creator"]
    }
    Post.create_post(data)
    return jsonify({"success": True, "messages": ["Post added successful!"]})  # Return success response


#show one post by id
@app.route('/posts/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    post_data = {
        "user_id": session['user_id']
    }
    data = {
        "id": id
    }

    logged_in_user = User.get_by_id(user_data)
    current_post = Post.show_post(data)
    post_adds = Post.get_all_post_adds(post_data)
    return render_template("showPost.html", logged_in_user = logged_in_user, current_post = current_post, post_adds = post_adds)

#route for update a post

@app.route('/posts/<int:id>/edit')
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id'],
    }
    data = {
        "id": id
    }

    logged_in_user = User.get_by_id(user_data)
    current_post = Post.show_post(data)
    return render_template("editpost.html", logged_in_user = logged_in_user, current_post = current_post)

#update route
@app.route('/posts/<int:id>/update', methods=['POST'])
def update_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    is_valid, errors = Post.validate_post(request.form)
    if not is_valid:
         return jsonify({"success": False, "messages": errors}) #400  # Send errors to frontend
    data = {
        "id": request.form["post_id"],
        "topic": request.form["topic"],
        "subtopic": request.form["subtopic"],
        "description": request.form["description"]
    }

    Post.update_post(data)
    return jsonify({"success": True, "messages": ["Post updated successfully!"]})  # Return success response
#delete route
@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    
    Post.destroy_post(data)
    return redirect('/posts')
# add listing  route
@app.route('/posts/<int:id>/add')
def add_topic(id):
    if 'user_id' not in session:
     return redirect('/logout')

    data = {
        "user_id": session['user_id'],
        "topic_id": id
    }
    
    Post.add_topic(data)
    return redirect('/posts')

# remove from listing
@app.route('/posts/<int:id>/remove')
def remove_topic(id):
    if 'user_id' not in session:
     return redirect('/logout')
    data = {
        "user_id": session['user_id'],
        "topic_id": id
    }

    Post.remove_topic(data)
    return redirect('/posts')

