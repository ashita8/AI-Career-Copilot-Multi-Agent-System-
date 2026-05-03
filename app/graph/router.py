from app.services.groq_client import llm

# -----------------------------------
# MAIN ROUTER (START)
# -----------------------------------
def route_request(state):
    message = state.get("message", "").strip()

    prompt = f"""
You are a routing AI.

Choose ONE route:

resume_agent
goal_agent
project_agent
roadmap_agent
general_chat_agent

User message:
{message}

Return only route name.
"""

    result = llm.invoke(prompt)
    route = result.content.strip().lower()

    allowed = {
        "resume_agent",
        "goal_agent",
        "project_agent",
        "roadmap_agent",
        "general_chat_agent"
    }

    if route in allowed:
        return route

    return "general_chat_agent"


# -----------------------------------
# AFTER RESUME ROUTER
# -----------------------------------
def route_after_resume(state):
    message = state.get("message", "").strip()

    prompt = f"""
Resume has already been analyzed.

Choose ONE next route:

project_agent
skill_gap_agent
roadmap_agent
end

Rules:
project_agent = asks for projects / portfolio / what to build
skill_gap_agent = compare resume vs JD / missing skills
roadmap_agent = asks roadmap / plan / next steps
end = only resume analysis needed

User message:
{message}

Return only route name.
"""

    result = llm.invoke(prompt)
    route = result.content.strip().lower()

    allowed = {
        "project_agent",
        "skill_gap_agent",
        "roadmap_agent",
        "end"
    }

    if route in allowed:
        return route

    return "end"