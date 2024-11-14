from flask import Flask
from pymongo import MongoClient
import config
from controllers.user_controller import user_blueprint
from controllers.question_controller import question_blueprint  # Import the new controller

app = Flask(__name__)
client = MongoClient(config.MONGO_URI)
db = client['quista_db']  # Use your database name
app.config['DB'] = db  # Store the database in app config for access in controllers

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(question_blueprint, url_prefix='/questions')  # Register the new blueprint

if __name__ == '__main__':
    app.run(debug=True)
