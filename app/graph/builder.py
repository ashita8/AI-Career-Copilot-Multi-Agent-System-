from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import CareerState
from app.graph.router import route_request

# Agents
from app.agents.goal_agent import goal_agent
from app.agents.skill_gap_agent import skill_gap_agent, jd_research_node
from app.agents.roadmap_agent import roadmap_agent
from app.agents.project_agent import project_agent
from app.agents.resume_agent import resume_agent
from app.agents.supervisor import general_chat_agent

# -----------------------------------
# Create Graph
# -----------------------------------
builder = StateGraph(CareerState)

# -----------------------------------
# Register Nodes
# -----------------------------------
builder.add_node("goal_agent", goal_agent)
builder.add_node("jd_research_node", jd_research_node)
builder.add_node("skill_gap_agent", skill_gap_agent)
builder.add_node("roadmap_agent", roadmap_agent)
builder.add_node("project_agent", project_agent)
builder.add_node("resume_agent", resume_agent)
builder.add_node("general_chat_agent", general_chat_agent)

# -----------------------------------
# START -> Router
# -----------------------------------
builder.add_conditional_edges(
    START,
    route_request,
    {
        "resume_agent": "resume_agent",
        "goal_agent": "goal_agent",
        "project_agent": "project_agent",
        "roadmap_agent": "roadmap_agent",
        "general_chat_agent": "general_chat_agent",
    }
)

# -----------------------------------
# Career Pipeline
# -----------------------------------
builder.add_edge("goal_agent", "jd_research_node")
builder.add_edge("jd_research_node", "skill_gap_agent")
builder.add_edge("skill_gap_agent", "roadmap_agent")
builder.add_edge("roadmap_agent", "project_agent")
builder.add_edge("project_agent", END)

# -----------------------------------
# Direct End Nodes
# -----------------------------------
builder.add_edge("resume_agent", END)
builder.add_edge("general_chat_agent", END)

# Optional direct routes
builder.add_edge("roadmap_agent", END)
builder.add_edge("project_agent", END)

# -----------------------------------
# Memory
# -----------------------------------
memory = MemorySaver()

graph = builder.compile(checkpointer=memory)

# -----------------------------------
# Export PNG
# -----------------------------------
png_data = graph.get_graph().draw_mermaid_png()

with open("career_copilot_graph.png", "wb") as f:
    f.write(png_data)

print("Saved graph image as career_copilot_graph.png")