# user_controller.py
from flask_app import app
from flask import flash
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
import requests
import json
from pprint import pprint
# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument

from flask_app.models.recipe_model import Recipe
#--------------------------------- index route ------------------------------------#
#index route
@app.route("/")
def index():
    
    return render_template("index.html")
@app.route("/create/cocktail", methods=["POST"])
def create_cocktail():
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    # response.json()
    # pprint(response.json())
    request_json = response.json()
    first_item = request_json["drinks"][0]
    # pprint(first_item)
    session["cocktail_id"] = first_item["idDrink"]
    session["name"] = first_item["strDrink"]
    
    # print("Cocktail_id", session["cocktail_id"])
    return render_template("cocktail.html", cocktail =  first_item)

#save route direct to login and reg page
@app.route("/reg&log")
def log_reg():
    return render_template("login.html")

#----------------Registration validation and create:-----------------#
@app.route("/users/registration", methods=["POST"])
def registration():
    #---------------Validate registration input----------------#
    #validate the user first, check the user is already in db
    if not User.validate_user(request.form):
        return redirect("/reg&log")
    #---------------Validate registration input---------------#
    # create the hash
    # print("User input password", request.form["password"])
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # print(pw_hash)
    # after password is hashed, create a new dictionary to hold all the validated 
    # data from the form and then send it to database using the create_user method
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }
    #put the validated request.form data into create_user method and store it in user_id
    user_id = User.create_user(new_user)
    #store "user_id" in session
    session["user_id"] = user_id
    #redirect to the dashboard, pay attention to the route in the wireframe
    return redirect("/recipes")

#------------------------- reder_template to "/recipes"------------------------#
#After passing the validation, redender_template to another html,
#and pass data to filled out the essential materials
@app.route("/recipes")
def recipes_dashboard():
#-----check the session["user_id"] exist, then that user can access the route --#
    if "user_id" in session:
        user_id = session["user_id"]
        data = {
            "user_id": user_id
        }
        #need a method to fetch data by the user_id(remember to put user_id in a dictionary)
        #and save that value to a variable
        current_user = User.get_user_by_id(data)
#--------------------------- second tables comes in to play --------------------------------#
        #get all the recipes from db and render those on the dashboard html
        #So you have to  import Recipe obj and method to do query select
        all_recipes = Recipe.read_all_recipes()
        #to display all_recipes you need to use jinja
        return render_template("recipes.html", current_user = current_user, recipes = all_recipes)
    else:
        return redirect("/")
#----------------------------Log Out-------------------------------#
@app.route("/users/login", methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect('/reg&log')
    #check if the email is already in db(registered)
    #we have the request.form data so we can use a method to 
    #check if that email is in db so create read_one_user_by_email
    data = {
        "email": request.form["email"]
    }
    #get the user id from email that is in DB
    user_in_db = User.read_one_user_by_email(data)
    #if the user_in_db is none then enter the flash, 
    #or user_in_db has a return value meaning the user exist we get his/her id
    #by calling read_one_user_by_email(data). Access the password that connected 
    #to the return value of read_one_user_by_email(data) and compare it with the 
    #password getting from the request.form. If not true, then flash the error msg
    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid email or password.","login")
        return redirect("/reg&log")
    #After validate the valid creds of user who log in
    #Use session to carry the "user_id" thru different route until we clear cookie
    session["user_id"] = user_in_db.id
    data = {
        "user_id" : session["user_id"],
        "cocktail_id" : session["cocktail_id"],
        "name": session["name"]
    }
    #each log in put one cocktail into DB
    Recipe.create_recipe(data)
    return redirect("/recipes")
    
#make a log out route and clear the session
@app.route("/logout")
def destroy_session():
    session.clear()
    print("Session is now cleared")
    return redirect("/")