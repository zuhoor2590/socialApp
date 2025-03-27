from flask_app.config.mysqlconnection import connectToMySQL
import re
import bcrypt  # Use bcrypt for secure password hashing


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "socialdb"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.email_hash = data['email_hash']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, email_hash, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(email_hash)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
    
    #method to validate registration serverside
    @staticmethod
    def validate_register(user):
        is_valid = True
        errors = []

        if len(user['first_name']) < 3:
            errors.append("First name must be at least 3 characters.")
            is_valid = False

        if len(user['last_name']) < 3:
            errors.append("Last name must be at least 3 characters.")
            is_valid = False
        # Check email format first before checking uniqueness
        if not EMAIL_REGEX.match(user['email']):
            errors.append("Invalid email format.")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(User.db_name).query_db(query, user)
            if len(results) >= 1:
                errors.append("Email already taken.")
                is_valid = False
                
        if len(user['password']) < 8:
            errors.append("Password must be at least 8 characters.")
            is_valid = False

        if user['password'] != user['confirm']:
            errors.append("Passwords do not match.")
            is_valid = False

        return is_valid, errors  # Return errors list instead of using `flash()`

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))