from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel as BM
from pydantic import Field as F
from typing import Any, List, Union


class Query(BM):
    """Query schema for the invoke endpoint"""

    input: str = F(description="The user query to the chatbot")
    session_id: str = F(
        description="A UUID which identifies this conversation over the chat storage"
    )

# TODO: Investigate why using the pydantic v2 BaseModel immplementation, this is not correctly recognised as a function which returns multiple arguments
class Response(BaseModel):
    """Final response schema to the question being asked"""

    answer: str = Field(description="The final answer to the user query.")
    sources: List[str] = Field(
        description="List of uuid that contain answer to the question. Only include an uuid if it contains relevant information."
    )
