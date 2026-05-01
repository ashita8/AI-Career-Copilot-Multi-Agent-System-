from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import CareerState

from app.agents.goal_agent import goal_agent
from app.agents.skill_gap_agent import skill_gap_agent ,jd_research_node

builder = StateGraph(CareerState)

# Register nodes
builder.add_node("goal_agent", goal_agent)
builder.add_node("jd_research_node", jd_research_node)
builder.add_node("skill_gap_agent", skill_gap_agent)

# Flow
builder.add_edge(START, "goal_agent")
builder.add_edge("goal_agent", "jd_research_node")
builder.add_edge("jd_research_node", "skill_gap_agent")
builder.add_edge("skill_gap_agent", END)

# Memory for HITL / resume
memory = MemorySaver()

graph = builder.compile(checkpointer=memory)