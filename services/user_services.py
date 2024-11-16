class UserService:
    def __init__(self, user_model):
        self.user_model = user_model

    def get_or_create_user(self, wallet_address):
        # Check if the user already exists
        existing_user = self.user_model.find_by_wallet(wallet_address)
        if existing_user:
            return self._format_user_data(existing_user), 200

        # Create a new user if not found (ensure atomicity using insert with unique constraint)
        try:
            self.user_model.insert_user(wallet_address)
        except Exception as e:
            # Handle cases where user might have been inserted in parallel requests
            existing_user = self.user_model.find_by_wallet(wallet_address)
            if existing_user:
                return self._format_user_data(existing_user), 200
            else:
                # Re-raise the exception if it's a different issue
                raise e

        new_user = self.user_model.find_by_wallet(wallet_address)  # Fetch the newly created user
        return self._format_user_data(new_user), 201

    def _format_user_data(self, user):
        # Return all relevant user attributes
        return {
            "wallet_address": user["wallet_address"],
            "daily_right": user.get("daily_right", 13),
            "eraser": user.get("eraser", 3),
            "balance": user.get("balance", 0.0),
            "earned_coins": user.get("earned_coins", 0.0),
            "seen_questions": user.get("seen_questions", []),
            "easy_count": user.get("easy_count", 0),
            "medium_count": user.get("medium_count", 0),
            "hard_count": user.get("hard_count", 0),
        }
