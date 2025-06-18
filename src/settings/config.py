import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("BOT_TOKEN")


# Language Model Configuration
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 500
LLM_MAX_RETRIES = 0

HABR_URL = f'https://habr.com/ru/hubs/artificial_intelligence/articles/'

PROMPT_TEMPLATE = """
Роль:
Ты полезный AI-ассистент, способный читать документы и выделять главную суть. 

Задача:
Прочитай HTML content и сделай следующее:
- внимательно изучи его
- перескажи краткое содержание в {paragraph_count}
- используй деловой стиль в ответе
- сохрани все важные цифры, имена и названия
- используй контекст документа в своем ответе
- строй предложения так, будто ты автор статьи

HTML Content:
{html_content}

Ответ:
"""

PG_CONN_PARAMS = {
    'host': 'db',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'dbname': 'users'
}
