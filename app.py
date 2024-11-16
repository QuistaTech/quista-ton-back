from flask import Flask
from pymongo import MongoClient
import config
from controllers.user_controller import user_blueprint
from controllers.question_controller import question_blueprint
from flask_cors import CORS

app = Flask(__name__)
client = MongoClient(config.MONGO_URI)
db = client['quista_db']
app.config['DB'] = db

# Register blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(question_blueprint, url_prefix='/questions')

# Initialize CORS and restrict it
CORS(app)  # Uncomment to allow all origins

# To disable CORS, specify restrictive options
#CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
