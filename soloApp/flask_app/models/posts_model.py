import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:

    db_name ="socialdb"

    def __init__(self,data):
        self.id = data['id']
        self.topic = data['topic']
        self.post = data['post']
        self.subtopic = data['subtopic']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users_who_add = []
#show all posts
    @classmethod
    def get_all_posts(cls):
        query = "SELECT posts.id, posts.topic, users.first_name AS creator, posts.subtopic FROM posts "\
        "JOIN users ON users.id = posts.user_id "\
        "LEFT JOIN adds ON posts.id = adds.topic_id "\
        "GROUP BY posts.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        # print(results)
        return results

    @classmethod
    def get_all_post_adds(cls, data):
        post_adds = []
        query = "SELECT topic_id FROM adds WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        # print(results)
        for result in results:
            post_adds.append(result['topic_id'])
        return post_adds
    #creating post
    @classmethod
    def create_post(cls, data):
        query = "INSERT into posts (topic, subtopic, description, user_id) VALUES (%(topic)s, %(subtopic)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    #get post by id 
    @classmethod
    def show_post(cls, data):
        query = "SELECT *, posts.id AS post_id, users.first_name AS creator FROM posts "\
        "JOIN users ON users.id = posts.user_id "\
        "WHERE posts.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        # print (results[0])
        return (results[0])
    

    #method to get the post and createor
    @classmethod
    def show_post_and_creator(cls, data):
        query = "SELECT *, users.first_name AS creator, posts.id AS number FROM users "\
        "LEFT JOIN posts ON users.id = posts.user_id "\
        "WHERE posts.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
    #update  post
    @classmethod
    def update_post(cls, data):
        query = "UPDATE posts SET topic = %(topic)s, subtopic = %(subtopic)s, description = %(description)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    #delete post 
    @classmethod
    def destroy_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    #add post to your listing
    @classmethod
    def add_topic(cls, data):
        query = "INSERT INTO adds (user_id, topic_id) VALUES (%(user_id)s, %(topic_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    #remove post from your listing
    @classmethod
    def remove_topic(cls, data):
        query = "DELETE from adds WHERE user_id = %(user_id)s AND topic_id = %(topic_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
#validation
    @staticmethod
    def validate_post(post):
        is_valid = True
        errors = []

        if len(post['topic']) < 1:
            errors.append("Topic field can not be left blank.")
            is_valid = False
            
        if len(post['subtopic']) < 1:
            errors.append("Title field can not be left blank.")
            is_valid = False
            
        if len(post['description']) < 1:
            errors.append("Description field can not be left blank.")
            is_valid = False
            
        return is_valid, errors