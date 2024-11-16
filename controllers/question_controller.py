from flask import Blueprint, request, jsonify, current_app
from services.quiz_services import QuizService
from models.question_model import QuestionModel
from models.user_model import UserModel

question_blueprint = Blueprint('question_controller', __name__)

def get_quiz_service(db):
    user_model = UserModel(db)
    question_model = QuestionModel(db)
    return QuizService(user_model, question_model)

@question_blueprint.route('/get_question/<string:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        db = current_app.config['DB']
        quiz_service = get_quiz_service(db)

        question = quiz_service.question_model.find_by_id(question_id)
        if not question:
            return jsonify({"success": False, "message": "Question not found."}), 404

        return jsonify({
            "success": True,
            "question": {
                "question_id": question["question_id"],
                "question_text": question["question_text"],
                "options": question["options"],  # Include options in the response
                "difficulty": question["difficulty"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500

@question_blueprint.route('/add_question', methods=['POST'])
def add_question():
    try:
        db = current_app.config['DB']
        quiz_service = get_quiz_service(db)

        question_id = request.json.get('question_id')
        question_text = request.json.get('question_text')
        options = request.json.get('options')  # Expecting options as a list
        correct_option = request.json.get('correct_option')  # Correct answer must match one of the options
        difficulty = request.json.get('difficulty', 1)

        if not question_id or not question_text or not options or not correct_option:
            return jsonify({"success": False, "message": "Missing required fields."}), 400

        if correct_option not in options:
            return jsonify({"success": False, "message": "Correct option must be one of the provided options."}), 400

        quiz_service.question_model.insert_question(question_id, question_text, options, correct_option, difficulty)

        return jsonify({"success": True, "message": "Question added successfully."}), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500

@question_blueprint.route('/feed_question', methods=['POST'])
def feed_question():
    try:
        db = current_app.config['DB']
        quiz_service = get_quiz_service(db)

        wallet_address = request.json.get('wallet_address')
        if not wallet_address:
            return jsonify({"success": False, "message": "Wallet address is required."}), 400

        question = quiz_service.get_next_question(wallet_address)
        if not question:
            return jsonify({"success": False, "message": "No more questions available for today."}), 403

        return jsonify({
            "success": True,
            "question": {
                "question_id": question["question_id"],
                "question_text": question["question_text"],
                "options": question["options"],  # Include options in the response
                "difficulty": question["difficulty"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500


    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500

@question_blueprint.route('/answer', methods=['POST'])
def answer_question():
    try:
        db = current_app.config['DB']
        quiz_service = get_quiz_service(db)

        wallet_address = request.json.get('wallet_address')
        question_id = request.json.get('question_id')
        selected_option = request.json.get('answer')  # Renamed to selected_option for clarity

        if not wallet_address or not question_id or not selected_option:
            return jsonify({"success": False, "message": "Missing required fields."}), 400

        response, status_code = quiz_service.process_answer(wallet_address, question_id, selected_option)
        return jsonify(response), status_code

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500
