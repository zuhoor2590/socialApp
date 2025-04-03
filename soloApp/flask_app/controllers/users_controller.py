from flask import render_template, redirect, session, request,jsonify
from flask_app import app
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
import hashlib

bcrypt = Bcrypt(app)

# Home page - root route
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard- checking user presence
@app.route('/register')
def signup():
    if 'user_id' in session:
        return redirect('/posts') #need to change to posts
    return render_template('register.html')

# Registration Logic (Now AJAX-friendly)
@app.route('/register', methods=['POST'])
def register():
    is_valid, errors = User.validate_register(request.form)

    if not is_valid:
        return jsonify({"success": False, "messages": errors})  # Send errors to frontend
    data = { 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "email_hash": hashlib.md5((request.form['email']).strip().lower().encode('utf-8')).hexdigest(),
        "password": bcrypt.generate_password_hash(request.form['password']).decode('utf-8')  # Ensure proper encoding
    }
    session['user_id'] = User.add(data)  # Add user to session
    return jsonify({"success": True, "messages": ["Registration successful!"]})  # Return success response


# Login Page
@app.route('/login')
def instructor_login():
    if 'user_id' in session:
        return redirect('/topics')
    return render_template('login.html')

# Login Logic (Now AJAX-friendly)
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email": request.form['email']})

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        return jsonify({"success": False, "messages": ["Invalid login credentials"]})  # AJAX response for errors

    session['user_id'] = user.id
    return jsonify({"success": True, "redirect_url": "/posts"})  # Send success response with redirect

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')