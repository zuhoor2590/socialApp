from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:

    db_name = "socialdb"

    def __init__(self,data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.topic_id=data['topic_id']
    #show all comments
    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments"
        results = connectToMySQL(cls.db_name).query_db(query)
        # print(results)
        return results

    @classmethod
    def get_all_post_comments(cls, data):
        query = "SELECT *, users.first_name AS commenter FROM comments "\
        "LEFT JOIN users on users.id = comments.user_id "\
        "WHERE topic_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    #adding comment method
    @classmethod
    def create_comment(cls, data):
        query = "INSERT into comments (comment, user_id, topic_id) VALUES (%(comment)s, %(user_id)s, %(topic_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    

    #update comment method
    @classmethod
    def update_comment(cls, data):
        query = "UPDATE comments SET comment = %(comment)s, updated_at = NOW() WHERE id = %(id)s"
        #query = "UPDATE comments SET comment = %(comment)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    #delete comment method
    @classmethod
    def remove_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    #validaition for comment form
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        errors = []
        comment_text = comment['comment'].strip()  # Remove leading/trailing spaces

        if len(comment_text) < 1:
            errors.append("Comment field cannot be left blank.")
            is_valid = False
        elif len(comment_text) >5000:
            errors.append("Comment must be under 5000 characters.")
            is_valid = False

        return is_valid, errors
        # if len(comment['comment']) < 1:
        #     errors.append("Comment field can not be left blank.")
        #     is_valid = False

        # return is_valid, errors