from typing import TypedDict, List
from langgraph.graph import StateGraph
import operator
from functools import reduce

class AgentState(TypedDict):
    values: List
    operation: int
    name: str
    result: str

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

def calculate(state: AgentState)-> AgentState:
    """This calculates the list if int and returns to the user"""

    symbol = state["operation"]
    nums = state["values"]

    op_function = OPERATORS.get(symbol, operator.add)

    total = reduce(op_function, nums)

    state["result"] = f"Hi {state['name']}, your answer is {total}"
    return state

graph = StateGraph(AgentState)

graph.add_node("calculater", calculate)

graph.set_entry_point("calculater")
graph.set_finish_point("calculater")

app = graph.compile()

answer = app.invoke({"values":[1,2,3,4], "name":"Steve", "operation":"*"})

print(answer["result"])


