from pymongo import MongoClient
from models.question_model import QuestionModel
MONGO_URI=""

client = MongoClient(MONGO_URI)  # Replace with your actual MongoDB URI
db = client['quista_db']
question_model = QuestionModel(db)

# List of questions to add
questions = [
    {
        "question_id": "3",
        "question_text": "What is 5 + 3?",
        "options": ["6", "7", "8", "9"],
        "correct_option": "8",
        "difficulty": 1
    },
    {
        "question_id": "4",
        "question_text": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "correct_option": "Mars",
        "difficulty": 1
    },
    {
        "question_id": "5",
        "question_text": "What is the square root of 144?",
        "options": ["10", "11", "12", "13"],
        "correct_option": "12",
        "difficulty": 2
    },
    {
        "question_id": "6",
        "question_text": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["Harper Lee", "J.K. Rowling", "Ernest Hemingway", "Mark Twain"],
        "correct_option": "Harper Lee",
        "difficulty": 2
    },
    {
        "question_id": "7",
        "question_text": "Which element has the chemical symbol 'Hg'?",
        "options": ["Helium", "Mercury", "Hydrogen", "Hafnium"],
        "correct_option": "Mercury",
        "difficulty": 3
    },
    {
        "question_id": "8",
        "question_text": "What is the derivative of x^2 with respect to x?",
        "options": ["2x", "x", "x^2", "1"],
        "correct_option": "2x",
        "difficulty": 3
    }
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

print("Questions added successfully.")
