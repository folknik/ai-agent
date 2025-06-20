from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from settings.config import *
from core.model import Response
from prompts.summary_agent_prompt import PROMPT_TEMPLATE


parser = PydanticOutputParser(pydantic_object=Response)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            PROMPT_TEMPLATE
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{html_content}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

llm = ChatOpenAI(
    model=LLM_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    max_retries=LLM_MAX_RETRIES
)

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[]
)


def run_agent(html_content: str) -> str:
    agent_executor = AgentExecutor(agent=agent, tools=[], verbose=False)
    raw_response = agent_executor.invoke({"html_content": html_content})
    structured_response = parser.parse(raw_response.get("output"))
    return structured_response.summary
