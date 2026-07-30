from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict): #state schema
    message : str

def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to this state"""

    state["message"] = "Hey "+ state["message"] +", how is your day going?"

    return state

# building the graph
graph = StateGraph(AgentState)

# building the node
graph.add_node("greeter", greeting_node)

# the starting and the ending point
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

result = app.invoke({"message":"Bob"})

print(result["message"])