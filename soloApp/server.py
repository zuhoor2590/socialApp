from flask_app import app
# DON'T FORGET TO IMPORT ALL YOUR CONTROLLERS!!!
from flask_app.controllers import users_controller, posts_controller, comments_controller
# ...server.py
if __name__=="__main__":
    app.run(debug=True)
