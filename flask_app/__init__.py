# __init__.py
from flask import Flask
app = Flask(__name__)


app.secret_key = "shhhhhh"


#connect to DB 
#Don't have to put db name each time

DB="recipes_db"