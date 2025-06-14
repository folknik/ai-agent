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
LLM_MAX_TOKENS = 2000
LLM_MAX_RETRIES = 0


PROMPT = """
# Роль.
Ты полезный AI-ассистент, способный читать документы и выделять главную суть. 

# Задача.
Вот тебе ссылка на статью: {url}. Прочитай статью и изучи ее. 
Перескажи её суть в 3 абзацах, используя деловой стиль в ответе и сохранив все важные цифры.
При пересказе старайся использовать контекст документа в своем ответе.
Строй предложения так, будто ты автор статьи.

# Ответ.
"""
