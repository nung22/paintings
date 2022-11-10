import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint
from flask_app.models import painting

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DATABASE = "paintings"

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.purchases = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # This method will validate form data for user objects
    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters.")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid email address.")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be longer than 8 characters.")
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Passwords do not match.")
        return is_valid
    
    # This method will create a new user object with given data
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # This method will retrieve a user object given its email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0:
            return User(result[0])
        else:
            return False
    
    # This method will retrieve a given user with all the paintings they have purchased.
    @classmethod
    def get_by_user_id(cls , data):
        query = "SELECT * FROM users LEFT JOIN purchases ON purchases.user_id = users.id LEFT JOIN paintings ON purchases.painting_id = paintings.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        user = cls( results[0] )
        for db_row in results:
            if db_row['paintings.id'] == None:
                break
            painting_data = {
                    "id" : db_row["paintings.id"],
                    "title" : db_row["title"],
                    "first_name" : db_row["first_name"],
                    "last_name" : db_row["last_name"],
                    "description" : db_row["description"],
                    "price" : db_row["price"],
                    "quantity" : db_row["quantity"],
                    "num_purchased" : db_row["num_purchased"],
                    "created_at" : db_row["paintings.created_at"],
                    "updated_at" : db_row["paintings.updated_at"]
            }
            user.purchases.append( painting.Painting( painting_data ) )
        return user
    
    # This method adds a new painting to the user's purchase list
    @classmethod
    def make_purchase(cls, data):
        query = "INSERT INTO purchases (user_id, painting_id) VALUES (%(user_id)s, %(painting_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)