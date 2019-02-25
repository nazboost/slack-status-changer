import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
verification_token = os.environ.get('verification_token')
token = os.environ.get('token')