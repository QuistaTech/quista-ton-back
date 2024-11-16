from pymongo import MongoClient
from models.question_model import QuestionModel

MONGO_URI = "mongodb+srv://serdar:sanane2001.@quista-db.yuhsc.mongodb.net/?retryWrites=true&w=majority&appName=quista-db"  # Replace with your actual MongoDB URI
client = MongoClient(MONGO_URI)
db = client['quista_db']
question_model = QuestionModel(db)

# List of manually created questions (over 50)
questions = [
    # Easy Questions (Difficulty 1)
    {"question_id": "36", "question_text": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "correct_option": "4", "difficulty": 1},


    # Add more as needed...

]

# Add questions to the database
for question in questions:
    question_model.insert_question(
        question_id=question["question_id"],
        question_text=question["question_text"],
        options=question["options"],
        correct_option=question["correct_option"],
        difficulty=question["difficulty"]
    )

print("Over 50 questions added successfully.")
