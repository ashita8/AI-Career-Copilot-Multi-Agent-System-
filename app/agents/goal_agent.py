from langgraph.types import interrupt
from app.services.groq_client import llm
from app.schemas.goal_schema import GoalSchema


def query_is_clear(query: str):
    q = query.lower()

    has_role = any(x in q for x in [
        "engineer", "developer", "scientist",
        "ai", "genai", "ml"
    ])

    has_time = any(x in q for x in [
        "month", "months", "year", "years"
    ])

    has_background = any(x in q for x in [
        "java", "python", "backend",
        "frontend", "student", "experience"
    ])

    return has_role and has_time and has_background


def goal_agent(state):
    query = state["query"]

    structured_llm = llm.with_structured_output(GoalSchema)
    result = structured_llm.invoke(query)

    data = result.model_dump()

    # deterministic override
    if query_is_clear(query):
        data["needs_clarification"] = False
        data["clarification_questions"] = []

    if data["needs_clarification"]:
        answers = interrupt({
            "type": "clarification",
            "message": "Need more details before planning roadmap",
            "questions": data["clarification_questions"]
        })

        data["user_answers"] = answers

    return {
        "goal_data": data
    }