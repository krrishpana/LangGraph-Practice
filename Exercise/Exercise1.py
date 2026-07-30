from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message : str

def compliment_node(state: AgentState) -> AgentState:
    """Simple node that gives compliments to the user."""

    state["message"] = "hey " + state["message"] + ",you are getting really good at LangGraph."

    return state

graph = StateGraph(AgentState)

graph.add_node("complimenter", compliment_node)

graph.set_entry_point("complimenter")
graph.set_finish_point("complimenter")

app = graph.compile()

result = app.invoke({"message":"Krrishpana"})

print(result["message"])