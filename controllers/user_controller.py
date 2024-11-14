from flask import Blueprint, request, jsonify, current_app
from services.user_services import UserService
from models.user_model import UserModel

user_blueprint = Blueprint('user_controller', __name__)

def get_user_service(db):
    user_model = UserModel(db)
    return UserService(user_model)

@user_blueprint.route('/register', methods=['POST'])
def register_or_get_user():
    try:
        db = current_app.config['DB']  # Access the database from the app config
        user_service = get_user_service(db)

        # Get the wallet_address from the incoming request
        wallet_address = request.json.get('wallet_address')
        if not wallet_address:
            return jsonify({"success": False, "message": "Wallet address is required."}), 400

        # Check if the user exists, otherwise create a new user
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
