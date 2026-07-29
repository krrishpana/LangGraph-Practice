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


#Exercise

# class AgentState(TypedDict):
#     message : str

# def compliment_node(state: AgentState) -> AgentState:
#     """Simple node that gives compliments to the user."""

#     state["message"] = "hey " + state["message"] + ",you are getting really good at LangGraph."

#     return state

# graph = StateGraph(AgentState)

# graph.add_node("complimenter", compliment_node)

# graph.set_entry_point("complimenter")
# graph.set_finish_point("complimenter")

# app = graph.compile()

# result = app.invoke({"message":"Krrishpana"})

# print(result["message"])


