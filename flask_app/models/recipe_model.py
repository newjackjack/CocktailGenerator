from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB
#put class object constructor, attributes, and methods in model 
import re	# the regex module
# create a regular expression object that we'll use later  

from flask_app.models.user_model import User 


class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.cocktail_id = data["cocktail_id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
#------------------------------------ Validate recipe --------------------------------#
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        
        return is_valid
#------------------------------------ Create recipe ---------------------------------#
    #create a recipe method
    @classmethod
    def create_recipe(cls,data):
        query = """
        INSERT INTO recipes (user_id, cocktail_id, name)
        VALUES(%(user_id)s,%(cocktail_id)s,%(name)s)
        """
        #don't forget to put foreign key
        results = connectToMySQL(DB).query_db(query,data)

        return results
#------------------------------------ Read all recipes ---------------------------------#
    #Read all recipes method
    @classmethod 
    def read_all_recipes(cls):
        query = """
        SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(DB).query_db(query)
        #results will be a list of dictionaries
        all_recipes = []
        for row in results:
            recipe = cls(row)
            # user_data = {
            #     **row,
            # }
            #
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            #put the user_data to the User class and call it creator
            #create a new "key" called creator and its value is the instance of User class from user_data
            recipe.creator = User(user_data)
            all_recipes.append(recipe)
        
        return all_recipes
#------------------------------------ Read one recipe ---------------------------------#
    #create a read_one_recipe method
    @classmethod
    def read_one_recipe(cls,data):
        query = """
        SELECT * FROM recipes WHERE id = %(id)s
        """
        result = connectToMySQL(DB).query_db(query,data)
        # print(result)

        return cls(result[0])
#------------------------------------ Update a recipe ---------------------------------#
    #create a method that update the recipe from the request.form
    @classmethod
    def update_recipe(cls,data):
        query = """
                UPDATE recipes SET name = %(name)s, 
                description = %(description)s,
                instruction = %(instruction)s,
                date_created = %(date_created)s, 
                under_thirty_minutes = %(under_thirty_minutes)s
                WHERE id = %(id)s;
            """
        results = connectToMySQL(DB).query_db(query,data)
        
        return results
#------------------------------------ Delete a recipe ---------------------------------#
    # create a method to delete recipe
    @classmethod
    def delete_recipe(cls,data):
        query = """
                DELETE FROM recipes WHERE id=%(id)s
        """
        result = connectToMySQL(DB).query_db(query,data)
        if result == None:
            return "success"
        else:
            return "failure"
