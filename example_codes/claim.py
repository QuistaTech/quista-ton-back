import requests

# Base URL for the answer endpoint
base_url = "http://127.0.0.1:5000/web3/claim"

# Example payload for submitting an answer
payload = {
    "wallet_address": "UQCaAgwsCXh4h15FAeQzWN22I655ZFg-JHg-XewLTReGcWNu",  # Replace with your actual wallet address
    "amount": "100",  # Replace with the question ID you received
}

# Sending the answer request
response = requests.post(base_url, json=payload)

# Print the response status code and text for debugging
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Handle the response
try:
    json_response = response.json()
    if response.status_code == 200:
        print(json_response.get("message"))
        print("User State:", json_response)
    else:
        print("Error:", json_response.get("message"))
except requests.exceptions.JSONDecodeError:
    print("Failed to parse JSON response.")
    print("Response content was:", response.text)
