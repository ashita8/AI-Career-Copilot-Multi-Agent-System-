from services.groq_client import llm
from schemas.project_schema import ProjectSchema


def project_agent(state):
    goal = state.get("goal_data", {})
    gap = state.get("skill_gap_data", {})
    roadmap = state.get("roadmap_data", {})

    role = goal.get("goal_title", "")
    level = goal.get("experience_level", "Intermediate")
    missing_skills = gap.get("missing_skills", [])

    structured_llm = llm.with_structured_output(ProjectSchema)

    prompt = f"""
You are an elite AI portfolio mentor.

Create portfolio projects for this user.

Target Role:
{role}

Experience Level:
{level}

Missing Skills:
{missing_skills}

Return:
- beginner_projects
- intermediate_projects
- advanced_projects
- must_have_portfolio_project
- github_strategy

Projects must help user get hired.
"""

    try:
        result = structured_llm.invoke(prompt)

        return {
            "project_data": result.model_dump()
        }

    except Exception:
        return {
            "project_data": {
                "beginner_projects": [
                    "Simple AI chatbot using FastAPI"
                ],
                "intermediate_projects": [
                    "RAG PDF assistant"
                ],
                "advanced_projects": [
                    "Multi-agent career copilot"
                ],
                "must_have_portfolio_project": {
                    "title": "Production AI Career Copilot",
                    "why": "Shows full-stack GenAI capability"
                },
                "github_strategy": [
                    "Pin top 3 repos",
                    "Write detailed README",
                    "Deploy live demo"
                ]
            }
        }