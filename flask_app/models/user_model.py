from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB
#put class object constructor, attributes, and methods in model 
import re	# the regex module
# create a regular expression object that we'll use later   


class User:
    def __init__(self,data):
        self.id = data["id"]#use hidden input
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
#----------------------------Registration Validation:-----------------------------#
    #create a user and validate user input
    #use static method because we don't necessarily need to channge instances
    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters.","registration")
            is_valid = False
            #so we need to use jinja in html to process the flash message,
            #remember to put category_filter in each flash messages
            
        #-----------------------------validate the last_name ------------------------------#
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters.","registration")
            is_valid = False
        #-----------------------------validate the email ------------------------------#
        #check if email is in correct length
        if len(user["email"]) < 3:
            flash("Email must be at least 3 characters.","registration")
            is_valid = False
        
        #check if email is in valid form
        #create a variable, EMAIL_REGEX
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        #check if the email exist in the db already
        #so we need a method, check_dabase which takes a dictionary this_user,
        # return results
        if (re.fullmatch(EMAIL_REGEX, user["email"])):
            this_user={
                "email": user["email"]
            }
            results = User.check_database(this_user)
            
            if len(results) != 0:
                flash("Email is already in use, please use a different email.","registration")
                is_valid = False
        #--------------------------------validate the password ------------------------------#
        #validate the password-length
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters.","registration")
            is_valid = False
         #check the password has at least one digit
        if(re.search('[0-9]', user['password'])== None):
            flash("Password requires at least one digit", "registration")
            print("If statement for checking password has one digit")
            is_valid = False
         #check the password has at least one upper case character
        if(re.search('[A-Z]', user['password'])== None):
            flash("Password requires at least one upper case character", "registration")
            print("If statement for checking password has one digit")
            is_valid = False
        #Check if password and confirm password are same
        #password 
        if (user["password"] != user["confirm_password"] ):
            flash("passwords do not match","registration")
            is_valid = False

        return is_valid
    
#----------------------------Login Validation:-----------------------------#
    # login validation 
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user["email"]) < 5 or len(user["password"]) < 8 :
            flash("Invalid email or password.","login")
            is_valid = False

        return is_valid
    
    #create a classmethod to check the db. Class method bc we need access to the class instance
    @classmethod
    def check_database(cls,data):
        query = """
                SELECT * FROM users WHERE email = %(email)s;
        """    
        results = connectToMySQL(DB).query_db(query,data)
        print("results from check_database",results)
        return results
    
#----------------------------------- Create User -----------------------------------------#
    #After validation and all the validations requirements pass
    #create user using class method
    @classmethod
    def create_user(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
        """
        #send query to connectToMySQL
        results = connectToMySQL(DB).query_db(query,data)
        #results will be the users.id 
        return results
        #after that we find the action route and method in html
        #which we have already called registration
#-------------------------------- Get one user by id ------------------------------------#
#------------ Read one user from db to display the user name on dashboard ---------------#
    @classmethod
    def get_user_by_id(cls,data):
        query="""
            SELECT * FROM users WHERE id = %(user_id)s;
        """
        result = connectToMySQL(DB).query_db(query, data)
        #since we only need one user so it return back a list of dictionary
        #but only has one element in that list
        # print("The result from get_user_by_id: ",result)
        return result[0]
#---------------------------login------------------------#
    @classmethod
    def read_one_user_by_email(cls,data):
        query = """
            SELECT * FROM users WHERE email = %(email)s
        """
        results = connectToMySQL(DB).query_db(query,data)
        #if not results means if result has a return value then return 
        if not results:
            return None
        return User(results[0])