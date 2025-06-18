import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("BOT_TOKEN")


# Language Model Configuration
LLM_MODEL = "gpt-4.1-mini"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 500
LLM_MAX_RETRIES = 0

HABR_URL = f'https://habr.com/ru/hubs/artificial_intelligence/articles/'

PG_CONN_PARAMS = {
    'host': 'db',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'dbname': 'users'
}
