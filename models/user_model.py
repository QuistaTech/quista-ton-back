class UserModel:
    def __init__(self, db):
        self.collection = db['users']
        self.ensure_collection_exists()

    def ensure_collection_exists(self):
        if not self.collection.index_information():
            self.collection.create_index("wallet_address", unique=True)

    def find_by_wallet(self, wallet_address):
        return self.collection.find_one({"wallet_address": wallet_address})

    def insert_user(self, wallet_address):
        user_data = {
            "wallet_address": wallet_address,
            "daily_right": 13,
            "eraser": 3,
            "earned_coins": 0.0,  # Only keep earned_coins
            "seen_questions": [],  # Initialize seen_questions as an empty list
            "easy_count": 0,       # Track number of easy questions answered
            "medium_count": 0,     # Track number of medium questions answered
            "hard_count": 0        # Track number of hard questions answered
        }
        self.collection.insert_one(user_data)


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
