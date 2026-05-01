from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import CareerState
from app.agents.goal_agent import goal_agent

builder = StateGraph(CareerState)

builder.add_node("goal_agent", goal_agent)

builder.add_edge(START, "goal_agent")
builder.add_edge("goal_agent", END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)