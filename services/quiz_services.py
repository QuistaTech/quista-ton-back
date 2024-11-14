class QuizService:
    def __init__(self, user_model, question_model):
        self.user_model = user_model
        self.question_model = question_model

    def get_next_question(self, wallet_address):
        user = self.user_model.find_by_wallet(wallet_address)
        if not user or user['daily_right'] <= 0:
            return None  # User has no more questions available for today

        # Define daily quota for question difficulties
        daily_quota = {1: 5, 2: 4, 3: 4}
        seen_questions = user.get('seen_questions', [])
        available_difficulties = self.get_available_difficulties(user, daily_quota)

        if not available_difficulties:
            return None

        for difficulty in available_difficulties:
            question = self.question_model.find_unseen_question(difficulty, seen_questions)
            if question:
                user['seen_questions'].append(question['question_id'])
                user['daily_right'] -= 1
                if difficulty == 1:
                    user['easy_count'] = user.get('easy_count', 0) + 1
                elif difficulty == 2:
                    user['medium_count'] = user.get('medium_count', 0) + 1
                elif difficulty == 3:
                    user['hard_count'] = user.get('hard_count', 0) + 1
                self.user_model.update_user(user)
                return question

        return None

    def process_answer(self, wallet_address, question_id, selected_option):
        user = self.user_model.find_by_wallet(wallet_address)
        if not user:
            return {"success": False, "message": "User not found."}, 404

        if user['daily_right'] <= 0:
            return {"success": False, "message": "No remaining questions for today."}, 403

        question = self.question_model.find_by_id(question_id)
        if not question:
            return {"success": False, "message": "Invalid question."}, 400

        correct_option = question['correct_option']
        if selected_option == correct_option:
            points = self.calculate_points(question['difficulty'])
            user['earned_coins'] += points
            message = f"Correct answer! You earned {points} points."
        else:
            if user['eraser'] > 0:
                user['eraser'] -= 1
                message = "Incorrect answer, but no points lost due to eraser."
            else:
                user['earned_coins'] -= 10  # Deduct points or handle as needed
                message = "Incorrect answer. Points deducted."
        user['daily_right'] -= 1
        user['seen_questions'].append(question_id)
        self.user_model.update_user(user)

        return {
            "success": True,
            "message": message,
            "user": {
                "wallet_address": user['wallet_address'],
                "daily_right": user['daily_right'],
                "eraser": user['eraser'],
                "earned_coins": user['earned_coins']
            }
        }, 200

    def get_available_difficulties(self, user, daily_quota):
        difficulty_count = {
            1: user.get('easy_count', 0),
            2: user.get('medium_count', 0),
            3: user.get('hard_count', 0)
        }
        available_difficulties = []
        for difficulty, max_count in daily_quota.items():
            if difficulty_count[difficulty] < max_count:
                available_difficulties.append(difficulty)
        return available_difficulties

    def calculate_points(self, difficulty):
        point_map = {1: 10, 2: 20, 3: 30}
        return point_map.get(difficulty, 10)
