import requests
import json

# Define the base URL of your Flask server
base_url = "http://127.0.0.1:5000/users/register"

def test_register_user(wallet_address):
    # Prepare the payload with the wallet address
    payload = {
        "wallet_address": wallet_address
    }

    # Make a POST request to the /register endpoint
    response = requests.post(base_url, json=payload)

    # Print the status code and response data
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    # Test with a new wallet address
    print("Testing with a new wallet address...")
    test_register_user("ttt")

    # Test with the same wallet address again to verify user retrieval
    print("\nTesting with the same wallet address (should retrieve existing user)...")
    test_register_user("ttt")
