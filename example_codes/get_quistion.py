import requests

# Define the endpoint URL
url = "http://127.0.0.1:5000/questions/start_quiz"

# Payload with wallet address
payload = {
    "wallet_address": "ttt"  # Replace with your actual wallet address
}

# Send POST request
response = requests.post(url, json=payload)

# Print the response
if response.status_code == 200:
    question = response.json().get("question")
    print(f"Question: {question['question_text']}")
    print(f"Options: {question['options']}")
else:
    print(response.json().get("message"))
