import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def process(state: AgentState) -> AgentState:
    """this node will solve the request you input"""
    response = llm.invoke(state['messages'][-5:])  # Use the last 5 messages for context
    
    state['messages'].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}\n")

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input = input("User: ")
while user_input.lower() != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result['messages']

    user_input = input("User: ")

with open("logging.txt", "w") as file:
    file.write("Your conversation log: \n")

    for messgae in conversation_history:
        if isinstance(messgae, HumanMessage):
            file.write(f"User: {messgae.content}\n")
        elif isinstance(messgae, AIMessage):
            file.write(f"AI: {messgae.content}\n")
    file.write("\nEnd of conversation log.")

print("Conversation log saved to logging.txt")