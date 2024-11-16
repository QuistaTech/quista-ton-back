from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB URI from the .env file
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)
