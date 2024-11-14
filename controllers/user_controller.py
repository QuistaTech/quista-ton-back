from flask import Blueprint, request, jsonify, current_app
from services.user_services import UserService
from models.user_model import UserModel

user_blueprint = Blueprint('user_controller', __name__)

def get_user_service(db):
    user_model = UserModel(db)
    return UserService(user_model)

@user_blueprint.route('/register', methods=['POST'])
def register_user():
    try:
        db = current_app.config['DB']  # Use current_app to access app context
        user_service = get_user_service(db)
        
        wallet_address = request.json.get('wallet_address')
        if not wallet_address:
            return jsonify({"success": False, "message": "Wallet address is required."}), 400
        
        response, status_code = user_service.register_user(wallet_address)
        
        # Ensure a successful operation returns "success": True
        if status_code == 200:
            result = {
                "success": True,
                "message": response.get("message", "Operation completed successfully.")
            }
        else:
            result = {
                "success": False,
                "message": response.get("message", "An error occurred during registration.")
            }

        return jsonify(result), status_code

    except Exception as e:
        # Handle unexpected errors and ensure consistent response structure
        result = {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }
        return jsonify(result), 500
