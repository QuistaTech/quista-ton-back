from flask import Blueprint, request, jsonify, current_app
from services.user_services import UserService
from models.user_model import UserModel
from services.web3_services import Web3Service
import asyncio

web3_blueprint = Blueprint('web3_controller', __name__)


def get_user_service(db):
    user_model = UserModel(db)
    return UserService(user_model)


@web3_blueprint.route('/claim', methods=['POST'])
def claim_tokens():
    try:
        db = current_app.config['DB']  # Access the database from the app config
        user_service = get_user_service(db)
        web3_service = Web3Service()

        # Get the wallet_address from the incoming request
        wallet_address = request.json.get('wallet_address')
        user, status_code = user_service.get_or_create_user(wallet_address)
        amount = user["balance"]

        if not wallet_address:
            return jsonify({"success": False, "message": "Wallet address is required."}), 400
        if amount == 0.0 or not amount:
            return jsonify({"success": False, "message": "Zero balance."}), 400
        try:
            # Claim the tokens asynchronously
            tx_hash = asyncio.run(web3_service.claim(wallet_address, amount))
            if "error" in tx_hash:
                return jsonify({"success": False, "message": tx_hash["error"]}), 400

            # Decrease the user's balance in the database
            user_service.user_model.decrease_balance(wallet_address, amount)

            # Respond with success
            return jsonify({
                "success": True,
                "tx_hash": tx_hash,
                "message": "Claimed successfully."
            })
        except Exception as e:
            return jsonify({"success": False, "message": f"Transaction failed: {e}"}), 400
    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({"success": False, "message": f"An unexpected error occurred: {e}"}), 500

