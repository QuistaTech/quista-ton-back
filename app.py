from flask import Flask
from pymongo import MongoClient
import config
from controllers.user_controller import user_blueprint

app = Flask(__name__)
client = MongoClient(config.MONGO_URI)
db = client['quista_db']  # Use the specified database
app.config['DB'] = db  # Storing the database in app config for access in controllers

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)
