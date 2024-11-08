from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, Sequence
from langchain_core.agents import AgentAction
import operator



# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], add_messages]

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
