from app.graph.state import CareerState


from app.services.groq_client import llm

def route_request(state):
    message = state.get("message", "")

    prompt = f"""
    You are a routing AI.

    Choose one route only:

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
    route = result.content.strip()

    allowed = {
        "resume_agent",
        "goal_agent",
        "project_agent",
        "roadmap_agent",
        "general_chat_agent"
    }

    if route not in allowed:
        return "general_chat_agent"

    return route