from app.services.groq_client import llm
from app.schemas.roadmap_schema import RoadmapSchema


def roadmap_agent(state):
    goal_data = state.get("goal_data", {})
    skill_gap = state.get("skill_gap_data", {})

    role = goal_data.get("goal_title", "")
    timeline = goal_data.get("timeline", "6 months")
    background = goal_data.get("current_background", "")

    missing_skills = skill_gap.get("missing_skills", [])
    level = skill_gap.get("readiness_level", "Intermediate")

    structured_llm = llm.with_structured_output(RoadmapSchema)

    prompt = f"""
You are an elite AI career planner.

Create a realistic roadmap for this user.

Target Role:
{role}

Timeline:
{timeline}

Current Background:
{background}

Readiness Level:
{level}

Missing Skills:
{missing_skills}

Return:
- phase_1 (foundation)
- phase_2 (intermediate)
- phase_3 (job ready)
- weekly_plan
- milestones
- daily_hours

Make roadmap practical and personalized.
"""

    try:
        result = structured_llm.invoke(prompt)

        return {
            "roadmap_data": result.model_dump()
        }

    except Exception:
        return {
            "roadmap_data": {
                "phase_1": ["Learn Python", "Learn FastAPI"],
                "phase_2": ["Learn RAG", "Build AI Apps"],
                "phase_3": ["Deploy portfolio", "Apply for jobs"],
                "weekly_plan": ["15 hrs/week"],
                "milestones": ["First AI app in 30 days"],
                "daily_hours": "2 hours/day"
            }
        }