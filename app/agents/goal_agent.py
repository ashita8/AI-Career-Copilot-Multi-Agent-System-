from langgraph.types import interrupt
from app.services.groq_client import llm
from app.schemas.goal_schema import GoalSchema


def goal_agent(state):
    query = state["query"]

    structured_llm = llm.with_structured_output(GoalSchema)
    result = structured_llm.invoke(query)

    data = result.model_dump()

    # If clear enough, continue normally
    if not data["needs_clarification"]:
        return {
            "goal_data": data
        }

    # Pause graph and ask human
    answers = interrupt({
        "type": "clarification",
        "message": "Need more details before planning roadmap",
        "questions": data["clarification_questions"]
    })

    # answers comes after resume
    return {
        "goal_data": data,
        "user_answers": answers
    }