from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]


@tool
def add(a:int, b:int):
    """This is an addition function that adds two numbers together"""

    return a + b

@tool
def subtract(a:int, b:int):
    """This is a subtraction function that subtracts the two numbers"""
    return a-b

@tool
def multiply(a:int, b:int):
    """This is a multiplication function that multiplies tht two numbers"""
    return a*b

tools = [add, subtract, multiply]

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash").bind_tools(tools)

def model_call(state:AgentState) ->AgentState:
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best ability.")
    response = model.invoke([system_prompt]+ state["messages"])
    return {"messages":[response]}


def should_continue(state:AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue":"tools",
        "end": END
    },
)

graph.add_edge("tools","our_agent")

app = graph.compile()

inputs = {"messages":[("user", "Add 3 + 4 and the subtract it by 4 and then tell me a joke" )]}
result = app.invoke(inputs)

for message in result["messages"]:
    message.pretty_print()


# print(result["messages"][-1].content)
