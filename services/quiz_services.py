import math


class QuizService:
    def __init__(self, user_model, question_model):
        self.user_model = user_model
        self.question_model = question_model

    def get_next_question(self, wallet_address):
        user = self.user_model.find_by_wallet(wallet_address)
        if not user or user['daily_right'] <= 0:
            return None  # User has no more questions available for today

        # Define question sequence based on the number of questions seen
        question_sequence = [1] * 5 + [2] * 3 + [3] * 2 + [4] * 2 + [5] * 1
        seen_questions = user.get('seen_questions', [])
        questions_seen_count = len(seen_questions)

        # If the user has already seen 13 questions, return None
        if questions_seen_count >= len(question_sequence):
            return None

        # Determine the difficulty for the next question based on the sequence
        next_difficulty = question_sequence[questions_seen_count]
        question = self.question_model.find_unseen_question(next_difficulty, seen_questions)

        if question:
            user['seen_questions'].append(question['question_id'])
            user['daily_right'] -= 1
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
        is_correct_answer = selected_option == correct_option
        tokens_added = 0

        if is_correct_answer:
            tokens_added = self.calculate_tokens(question['difficulty'])*self.calculate_multiplier(user)  # New token logic
            xp_added = self.calculate_xp_increment(question["difficulty"])
            user['balance'] = user.get('balance', 0) + tokens_added  # Add tokens to user balance
            user["xp"] = user.get("xp", 0) + xp_added
        else:
            if user['eraser'] > 0:
                user['eraser'] -= 1
            else:
                user['earned_coins'] -= 10  # Deduct points or handle as needed

        self.user_model.update_user(user)

        return {
            "success": True,
            "isCorrectAnswer": is_correct_answer,
            "tokensAdded": tokens_added,
            "user": {
                "wallet_address": user['wallet_address'],
                "daily_right": user['daily_right'],
                "eraser": user['eraser'],
                "balance": user.get('balance', 0)  # Return balance as part of response
            }
        }, 200

    def get_available_difficulties(self, user, daily_quota):
        difficulty_count = {
            1: user.get('easy_count', 0),  # 5
            2: user.get('medium_count', 0),  # 3
            3: user.get('hard_count', 0),  # 2
            4: user.get('very_hard_count', 0),  # 2
            5: user.get('legendary_count', 0)  # 1
        }
        available_difficulties = []
        for difficulty, max_count in daily_quota.items():
            if difficulty_count[difficulty] < max_count:
                available_difficulties.append(difficulty)
        return available_difficulties

    def calculate_tokens(self, difficulty):
        token_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}  # Example token distribution
        return token_map.get(difficulty, 1)

    def calculate_xp_increment(self, difficulty):
        xp_map = {1: 20, 2: 40, 3: 60, 4: 80, 5: 100}
        return xp_map[difficulty]

    def calculate_multiplier(self,user):
        level = math.floor(pow((70*user["xp"])/600,1/2.69))
        return pow(1.11,(level-1))
