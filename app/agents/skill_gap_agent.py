from services.tavily_search import search_jobs

def jd_research_node(state):
    role = state["goal_data"]["goal_title"]

    query = f"{role} job description required skills"

    results = search_jobs(query)

    return {
        "jd_data": results
    }

# app/agents/skill_gap_agent.py

from services.groq_client import llm
from schemas.skill_gap_schema import SkillGapSchema


def skill_gap_agent(state):
    """
    Inputs expected in state:
    - goal_data (dict)
    - jd_data (list or dict from Tavily search node)
    - user_answers (optional)
    
    Output:
    - skill_gap_data
    """

    goal_data = state.get("goal_data", {})
    jd_data = state.get("jd_data", [])
    user_answers = state.get("user_answers", "")

    role = goal_data.get("goal_title", "AI Engineer")
    background = goal_data.get("current_background", "Unknown")
    level = goal_data.get("experience_level", "Unknown")

    # Convert Tavily results into text context
    jd_context = ""

    if isinstance(jd_data, dict):
        results = jd_data.get("results", [])
        for item in results:
            title = item.get("title", "")
            content = item.get("content", "")
            jd_context += f"\nTitle: {title}\nContent: {content}\n"

    elif isinstance(jd_data, list):
        jd_context = "\n".join([str(x) for x in jd_data])

    structured_llm = llm.with_structured_output(SkillGapSchema)

    prompt = f"""
You are an expert AI career coach.

Analyze the user's current background and compare it with real-world market job requirements.

Target Role:
{role}

Current Background:
{background}

Experience Level:
{level}

Additional User Info:
{user_answers}

Job Market Data:
{jd_context}

Return structured skill gap analysis.
"""

    try:
        result = structured_llm.invoke(prompt)

        return {
            "skill_gap_data": result.model_dump()
        }

    except Exception:
        return {
            "skill_gap_data": {
                "current_strengths": [],
                "missing_skills": [
                    "Python",
                    "FastAPI",
                    "LLM APIs",
                    "RAG",
                    "LangGraph"
                ],
                "priority_skills": [
                    "Python",
                    "FastAPI",
                    "LangGraph"
                ],
                "hiring_signals": [],
                "readiness_level": "Needs Assessment"
            }
        }