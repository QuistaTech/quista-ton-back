from flask import Blueprint, request, jsonify, current_app
from services.user_services import UserService
from models.user_model import UserModel
from services.quiz_services import QuizService

user_blueprint = Blueprint('user_controller', __name__)


def get_user_service(db):
    user_model = UserModel(db)
    return UserService(user_model)

@user_blueprint.route('<wallet_address>/level', methods=['GET'])
def get_user_level(wallet_address):
    try:
        # Access the database from the app configuration
        db = current_app.config['DB']

        # Get the user service instance
        user_service = get_user_service(db)

        # Retrieve the user by wallet address
        user = db.users.find_one({"wallet_address": wallet_address})
        if not user:
            return jsonify({"success": False, "message": "User not found."}), 404

        # Calculate the user's level based on their XP
        user_level = user_service.calculate_user_level(current_xp=user["xp"])

        # Prepare and return the response
        return jsonify({
            "success": True,
            "user_level": user_level,
            "message": "User level fetched successfully."
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@user_blueprint.route('/register', methods=['POST'])
def register_or_get_user():
    try:
        db = current_app.config['DB']  # Access the database from the app config
        user_service = get_user_service(db)

        # Get the wallet_address from the incoming request
        wallet_address = request.json.get('wallet_address')
        if not wallet_address:
            return jsonify({"success": False, "message": "Wallet address is required."}), 400

        # Check if the user exists, otherwise create a new user atomically
        user, status_code = user_service.get_or_create_user(wallet_address)

        result = {
            "success": True,
            "user": user,
            "message": "User retrieved or created successfully." if status_code == 201 else "User retrieved successfully."
        }
        return jsonify(result), status_code

    except Exception as e:
        # Handle unexpected errors with a consistent response structure
        result = {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }
        return jsonify(result), 500
