class QuestionModel:
    def __init__(self, db):
        self.collection = db['questions']

    def insert_question(self, question_id, question_text, options, correct_option, difficulty=1):
        question_data = {
            "question_id": question_id,
            "question_text": question_text,
            "options": options,
            "correct_option": correct_option,
            "difficulty": difficulty
        }
        self.collection.insert_one(question_data)

    def find_by_id(self, question_id):
        return self.collection.find_one({"question_id": question_id})

    def find_unseen_question(self, difficulty, seen_questions):
        return self.collection.find_one({
            "difficulty": difficulty,
            "question_id": {"$nin": seen_questions}
        })
