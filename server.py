from flask_app import app
#Connect to controllers
from flask_app.controllers import user_controller, recipe_controller
#connect to models
from flask_app.models.user_model import User




if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True, host="localhost", port=8000)    # Run the app in debug mode.
