class UserModel:
    def __init__(self, db):
        self.collection = db['users']  # Collection name
        self.ensure_collection_exists()

    def ensure_collection_exists(self):
        # Create a unique index on wallet_address to ensure no duplicates
        if not self.collection.index_information():
            self.collection.create_index("wallet_address", unique=True)

    def find_by_wallet(self, wallet_address):
        return self.collection.find_one({"wallet_address": wallet_address})

    def insert_user(self, wallet_address):
        user_data = {
            "wallet_address": wallet_address,
            "daily_right": 13,        # Default initial value
            "eraser": 3,            # Default initial value
            "earned_coins": 0.0,      # Default initial value
            "balance": 0.0            # Default initial value
        }
        self.collection.insert_one(user_data)
