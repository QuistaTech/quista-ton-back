class UserModel:
    def __init__(self, db):
        self.collection = db['users']
        # Ensure a unique index on wallet_address (if not already created)
        self.collection.create_index("wallet_address", unique=True)

    def find_by_wallet(self, wallet_address):
        return self.collection.find_one({"wallet_address": wallet_address})

    def insert_user(self, wallet_address):
        user_data = {
            "wallet_address": wallet_address,
            "daily_right": 13,
            "eraser": 3,
            "balance": 0.0,
            "earned_coins": 0.0,  # Only keep earned_coins
            "seen_questions": [],  # Initialize seen_questions as an empty list
            "easy_count": 0,  # Track number of easy questions answered
            "medium_count": 0,  # Track number of medium questions answered
            "hard_count": 0,  # Track number of hard questions answered
            "xp": 0
        }
        # Insert user data with error handling for duplicate key errors
        try:
            self.collection.insert_one(user_data)
        except Exception as e:
            if 'duplicate key error' in str(e):
                # Handle duplicate user insertion attempt gracefully
                raise Exception("User already exists")
            else:
                # Re-raise other exceptions
                raise e

    def update_user(self, user_data):
        self.collection.update_one(
            {"wallet_address": user_data["wallet_address"]},
            {"$set": user_data}
        )

    def add_seen_question(self, wallet_address, question_id, difficulty):
        # Find the user and update seen_questions list
        user = self.find_by_wallet(wallet_address)
        if user:
            user['seen_questions'].append(question_id)

            # Increment the difficulty count based on the question type
            if difficulty == 1:
                user['easy_count'] += 1
            elif difficulty == 2:
                user['medium_count'] += 1
            elif difficulty == 3:
                user['hard_count'] += 1

            self.update_user(user)

    def decrease_balance(self, wallet_address, amount):
        user = self.find_by_wallet(wallet_address)
        user["balance"] -= float(amount)
        self.update_user(user)
