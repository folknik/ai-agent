from langchain_openai import OpenAI

from settings.config import *


llm = OpenAI(
    model=LLM_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    max_retries=LLM_MAX_RETRIES
)


def run_agent(prompt: str, html_content: str) -> str:
    inputs = [
        {
            "role": "system",
            "content": prompt.format(html_content=html_content)
        }
    ]
    response = llm.invoke(inputs)
    return response
