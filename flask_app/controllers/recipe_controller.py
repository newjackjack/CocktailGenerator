from flask_app import app
from flask import flash
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
import requests
import json
from pprint import pprint
#------------------------- reder_template to create_recipe page------------------------#
#create recipe and render_template into create_recipe.html
@app.route("/recipes/new")
def show_create_recipe():
    #be able to avoid from someone who does not log in(just typing the url)
    if "user_id"  not in session:
        flash("You must be logged in to view this page","validate_recipe")
        return redirect("/create/cocktail")
    return render_template("create_recipe.html")
#------------------------- a route to handle the form in the create page------------------------#
#create recipe action:"/create/recipe", method = "post"
@app.route("/recipe/create", methods=["POST"])
def create_new_recipe():
    #first thing to do is validate the recipe
    if not Recipe.validate_recipe(request.form):
        return redirect("/create/cocktail")
    # print(request.form)
    #request.form should have validation so need a validate recipe method
    #after validation, store the request.form data to data dictionary
    data ={
        "user_id": session["user_id"],
        "cocktail_id":session["cocktail_id"],
        "instruction":request.form["instruction"],
        "date_created":request.form["date_created"],
        "under_thirty_minutes":request.form["under_thirty_minutes"]
    }
    #------------------------create recipe --------------------------#
    #submit to create recipe
    Recipe.create_recipe(data)
    # after creating the recipe, need to display all the recipes on the recipes page
    # so, we need a get all recipes method
    return redirect("/recipes")
    #bc "/recipes" has called read_all_recipes method in Recipe class
#--------------------------------view one recipe ---------------------------------#
    #A route to view specific recipe by its recipes' id
    #need to go back to dashboard(recipe.html ) and figure out the recipe_id
@app.route("/recipes/<int:recipe_id>")
def show_one_recipe(recipe_id):
    #check if the user_id is in session
    if "user_id" not in session:
        flash("You must be logged in to view this page", "validate_login")
        session.clear()
        return redirect("/")
    #do somethig to id --> make id to a dictionary
    data = {
        "id": recipe_id
    }
    #call a method, read_one_recipe which takes the linked id and fetch the recipe
    one_recipe = Recipe.read_one_recipe(data)
    
    # read_one_recipe only gives you one recipe, but we still need to show the creator
    user_id = {
        "user_id": session["user_id"]
    }
    current_user = User.get_user_by_id(user_id)
    #----------------view one recipe call the api again------------#
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={one_recipe.cocktail_id}')
    response.json()
    request_json = response.json()
    first_item = request_json["drinks"][0]
    
    return render_template("view_recipe.html",cocktail =  first_item)
#--------------------------------edit one recipe ---------------------------------#
# route to edit_recipe page
@app.route("/recipes/edit/<int:recipe_id>")
def edit_one_recipe(recipe_id):
    #check if user_id is in session
    if "user_id" not in session:
        flash("You must be logged in to edit", "validate_login")
        session.clear()
        return redirect("/")
    #put the linked id into data dictionary and put it to read_one recipe
    #so that we can render previous data as value in the input tag in edit_recipe.html
    data = {
        "id": recipe_id
    }
    recipe = Recipe.read_one_recipe(data)
    #recipe get pushed in render template so the html knows the original data input of the recipe
    return render_template("edit_recipe.html", recipe = recipe)
#-------------------------------- handle edit  ---------------------------------#
@app.route("/recipes/edit",methods = ["POST"])
def edit_recipe():
    #make a data dictionary to store data from request.form
    #*****************user_id is passed from the session *********************#
    data = {
        "id":request.form["id"],#from input hidden
        "user_id": session["user_id"],
        #One can only see the edit and edit is the creator of this recipe
        "name":request.form["name"],
        "description":request.form["description"],
        "instruction":request.form["instruction"],
        "date_created":request.form["date_created"],
        "under_thirty_minutes":request.form["under_thirty_minutes"]
    }
    id = request.form["id"]
    #validate the edit request.form
    # print("id:", id)
    #validate the recipe to see if they meet the requirements
    if not Recipe.validate_recipe(data):
        print("Validate edit not passed")
        return redirect(f"/recipes/edit/{id}")
    # After validate the edit, update the data in db by calling the method
    Recipe.update_recipe(data)
    return redirect("/recipes")
#-------------------------------- delete recipe ---------------------------------#
#delete route
@app.route("/recipes/delete/<int:recipe_id>")
def delete(recipe_id):

    this_recipe = {
        "id": recipe_id
    }
    Recipe.delete_recipe(this_recipe)
    return redirect("/recipes")