import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT"))

API_KEY = os.getenv("API_KEY")

API_KEY_NAME = os.getenv("API_KEY")

SWAGGER_USERNAME = os.getenv("SWAGGER_USERNAME")

SWAGGER_PASSWORD = os.getenv("SWAGGER_PASSWORD")

DATABASE_URL = os.getenv("DATABASE_URL")

