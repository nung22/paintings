import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint

DATABASE = "paintings"

class Painting:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.num_purchased = data['num_purchased']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # This method will validates form data for painting objects
    @staticmethod
    def validate_painting(painting:dict) -> bool:
        is_valid = True
        if len(painting['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters.")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters.")
        if float(painting['price']) < 0.01:
            is_valid = False
            flash("Price must be greater than 0.")
        if int(painting['quantity']) < 1:
            is_valid = False
            flash("Quantity must be greater than 0.")
        return is_valid
    
    # This method will return all instance of painting objects
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings JOIN users ON users.id = paintings.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        paintings = []
        for painting in results:
            paintings.append( cls(painting) )
        return paintings
    
    # This method will create a new painting object with given data
    @classmethod
    def save(cls, data):
        query = "INSERT INTO paintings (user_id, title, description, price, quantity, num_purchased) VALUES (%(user_id)s, %(title)s, %(description)s, %(price)s, %(quantity)s, %(num_purchased)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # This method will get a painting object given its id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM paintings JOIN users on users.id = paintings.user_id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        painting = Painting( results[0] )
        return painting
    
    # This method will edit a painting object given its id and any new data
    @classmethod
    def edit(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s WHERE paintings.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def buy(clas, data):
        query = "UPDATE paintings SET quantity = %(quantity)s, num_purchased = %(num_purchased)s  WHERE paintings.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # This method will delete a painting object given its id
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM paintings WHERE paintings.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
