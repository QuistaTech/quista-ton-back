Quiz API Documentation
----------------------

### Base URL

arduino

Copy code

`http://127.0.0.1:5000`

* * * * *

### 1\. `POST /questions/add_question`

#### Description

Adds a new multiple-choice question to the database.

#### Request

-   **URL**: `/questions/add_question`
-   **Method**: `POST`
-   **Headers**: `Content-Type: application/json`
-   **Payload**:

    json

    Copy code

    `{
        "question_id": "unique_question_id",
        "question_text": "Your question text here",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_option": "Option 3",
        "difficulty": 2  // Difficulty levels: 1 (Easy), 2 (Medium), 3 (Hard)
    }`

#### Response

-   **Success (201 Created)**:

    json

    Copy code

    `{
        "success": true,
        "message": "Question added successfully."
    }`

-   **Error (400 Bad Request)**:

    json

    Copy code

    `{
        "success": false,
        "message": "Missing required fields."
    }`

* * * * *

### 2\. `GET /questions/get_question/<question_id>`

#### Description

Fetches a specific question by its `question_id`.

#### Request

-   **URL**: `/questions/get_question/<question_id>`
-   **Method**: `GET`

#### Response

-   **Success (200 OK)**:

    json

    Copy code

    `{
        "success": true,
        "question": {
            "question_id": "unique_question_id",
            "question_text": "Your question text here",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "difficulty": 2
        }
    }`

-   **Error (404 Not Found)**:

    json

    Copy code

    `{
        "success": false,
        "message": "Question not found."
    }`

* * * * *

### 3\. `POST /questions/start_quiz`

#### Description

Starts a quiz for a user by providing the next available question based on their daily progress and seen questions.

#### Request

-   **URL**: `/questions/start_quiz`
-   **Method**: `POST`
-   **Headers**: `Content-Type: application/json`
-   **Payload**:

    json

    Copy code

    `{
        "wallet_address": "user_wallet_address"
    }`

#### Response

-   **Success (200 OK)**:

    json

    Copy code

    `{
        "success": true,
        "question": {
            "question_id": "unique_question_id",
            "question_text": "Your question text here",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "difficulty": 1
        }
    }`

-   **Error (403 Forbidden)**:

    json

    Copy code

    `{
        "success": false,
        "message": "No more questions available for today."
    }`

-   **Error (400 Bad Request)**:

    json

    Copy code

    `{
        "success": false,
        "message": "Wallet address is required."
    }`

* * * * *

### 4\. `POST /questions/answer`

#### Description

Submits an answer for a specific question by a user.

#### Request

-   **URL**: `/questions/answer`
-   **Method**: `POST`
-   **Headers**: `Content-Type: application/json`
-   **Payload**:

    json

    Copy code

    `{
        "wallet_address": "user_wallet_address",
        "question_id": "unique_question_id",
        "answer": "selected_option"
    }`

#### Response

-   **Success (200 OK)**:

    json

    Copy code

    `{
        "success": true,
        "message": "Correct answer! You earned 10 points.",
        "user": {
            "wallet_address": "user_wallet_address",
            "daily_right": 12,
            "eraser": 3,
            "earned_coins": 20.0
        }
    }`

-   **Error (404 Not Found)**:

    json

    Copy code

    `{
        "success": false,
        "message": "User not found."
    }`

-   **Error (400 Bad Request)**:

    json

    Copy code

    `{
        "success": false,
        "message": "Missing required fields."
    }`

-   **Error (403 Forbidden)**:

    json

    Copy code

    `{
        "success": false,
        "message": "No remaining questions for today."
    }`

* * * * *

### Guidelines and Notes

1.  **Question Difficulty**:

    -   `1` = Easy
    -   `2` = Medium
    -   `3` = Hard
2.  **User Attributes**:

    -   `wallet_address`: Unique identifier for each user.
    -   `daily_right`: Number of questions the user can answer per day (decrements with each question).
    -   `eraser`: Number of times the user can make a mistake without penalty.
    -   `earned_coins`: Tracks the points earned by the user.
3.  **Question Storage**:

    -   Questions are stored with the following attributes: `question_id`, `question_text`, `options`, `correct_option`, and `difficulty`.
    -   Ensure each `question_id` is unique.
4.  **Multiple-Choice Questions**:

    -   `options` is an array containing possible answers.
    -   `correct_option` is the correct answer and must be one of the values in `options`.

### Example Usage Flow

1.  **Add a Question**:
    -   POST to `/questions/add_question` with the question details.
2.  **Start a Quiz**:
    -   POST to `/questions/start_quiz` with the user's `wallet_address`.
3.  **Get a Question**:
    -   Use the returned question from the `start_quiz` response.
4.  **Answer a Question**:
    -   POST to `/questions/answer` with the user's `wallet_address`, `question_id`, and the `selected_option`.