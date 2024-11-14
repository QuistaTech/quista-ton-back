class UserService:
    def __init__(self, user_model):
        self.user_model = user_model

    def get_or_create_user(self, wallet_address):
        # Check if the user already exists
        existing_user = self.user_model.find_by_wallet(wallet_address)
        if existing_user:
            return {
                "wallet_address": existing_user["wallet_address"],
                "daily_right": existing_user["daily_right"],
                "eraser": existing_user["eraser"],
                "earned_coins": existing_user["earned_coins"],
            }, 200

        # Create a new user if not found
        self.user_model.insert_user(wallet_address)
        new_user = self.user_model.find_by_wallet(wallet_address)  # Fetch the newly created user
        return {
            "wallet_address": new_user["wallet_address"],
            "daily_right": new_user["daily_right"],
            "eraser": new_user["eraser"],
            "earned_coins": new_user["earned_coins"],
        }, 201
