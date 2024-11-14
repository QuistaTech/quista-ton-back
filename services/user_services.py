class UserService:
    def __init__(self, user_model):
        self.user_model = user_model

    def register_user(self, wallet_address):
        if not wallet_address:
            return {"error": "Wallet address is required"}, 400

        existing_user = self.user_model.find_by_wallet(wallet_address)
        if existing_user:
            return {"message": "Wallet address already registered"}, 400

        self.user_model.insert_user(wallet_address)
        return {"message": f"User with wallet {wallet_address} registered successfully"}, 201
