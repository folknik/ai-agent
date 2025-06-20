from pydantic import BaseModel


class Response(BaseModel):
    topic: str
    summary: str
    # sources: str
    # list_tools: list[str]
