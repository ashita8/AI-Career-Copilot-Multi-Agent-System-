from langgraph.graph import StateGraph, END
from app.graph.state import CareerState
from app.agents.goal_agent import run_goal_agent

builder = StateGraph(CareerState)

builder.add_node("goal", run_goal_agent)

builder.set_entry_point("goal")
builder.add_edge("goal", END)

graph = builder.compile()