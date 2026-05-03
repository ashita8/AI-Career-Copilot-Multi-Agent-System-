from langgraph.types import interrupt
from services.groq_client import llm
from schemas.goal_schema import GoalSchema,FollowupSchema

def needs_more_info(data):
    required = [
        data.get("goal_title"),
        data.get("timeline"),
        data.get("current_background")
    ]

    return any(x in [None, "", "Unknown"] for x in required)

# Deterministic clarity check
def query_is_clear(query: str):
    q = query.lower()

    has_role = any(x in q for x in [
        "engineer", "developer", "scientist",
        "ai", "gen ai", "genai", "ml"
    ])

    has_time = any(x in q for x in [
        "month", "months", "year", "years"
    ])

    has_background = any(x in q for x in [
        "java", "python", "backend",
        "frontend", "student", "fresher",
        "experience", "years exp"
    ])

    # MUST HAVE ALL THREE
    return has_role and has_time and has_background


# Generate deterministic clarification questions
def build_clarification_questions(data):
    questions = []

    if not data.get("current_background") or data["current_background"].lower() in ["unknown", "", "none"]:
        questions.append("What is your current background? (student / developer / fresher / etc.)")

    if not data.get("experience_level") or data["experience_level"].lower() in ["unknown", "", "none"]:
        questions.append("How much experience do you have?")

    if not data.get("timeline") or data["timeline"].lower() in ["unknown", "", "none"]:
        questions.append("What timeline are you targeting? (3 months / 6 months / 1 year)")

    # max 3 for better UX
    return questions[:3]



def normalize_empty(data):
    """
    convert guessed / junk values into None
    """
    bad = ["unknown", "none", "null", "", "long-term"]

    for key in ["timeline", "current_background", "experience_level"]:
        val = data.get(key)

        if val is None:
            continue

        if isinstance(val, str) and val.strip().lower() in bad:
            data[key] = None

    return data


def extract_followup(answer_text):
    """
    LLM structured extractor for follow-up answer
    """
    parser_llm = llm.with_structured_output(FollowupSchema)

    prompt = f"""
Extract only explicitly mentioned fields from this user reply.

Rules:
- Do NOT guess.
- If timeline not mentioned -> null
- If background not mentioned -> null
- If experience level not mentioned -> null
- Convert years experience to level:
  0-1 = Beginner
  2-4 = Intermediate
  5+ = Advanced

User reply:
{answer_text}
"""

    result = parser_llm.invoke(prompt)
    return result.model_dump()


def goal_agent(state):
    query = state.get("message") or state.get("query", "")

    # --------------------------------
    # Initial extraction
    # --------------------------------
    try:
        structured_llm = llm.with_structured_output(GoalSchema)

        prompt = f"""
        Extract user career goal.

        Rules:
        - Do NOT guess missing fields.
        - If timeline not present -> null
        - If background not present -> null
        - If level not present -> null

        User query:
        {query}
        """

        result = structured_llm.invoke(prompt)
        data = result.model_dump()

    except Exception:
        data = {
            "goal_title": query,
            "timeline": None,
            "current_background": None,
            "experience_level": None,
        }

    data = normalize_empty(data)

    # --------------------------------
    # HITL LOOP
    # --------------------------------
    while True:

        questions = build_clarification_questions(data)

        if not questions:
            data["needs_clarification"] = False
            data["clarification_questions"] = []
            break

        data["needs_clarification"] = True
        data["clarification_questions"] = questions

        answer = interrupt({
            "type": "clarification",
            "message": "Need a few details before creating your personalized roadmap",
            "questions": questions
        })

        # structured extraction from followup
        parsed = extract_followup(answer)

        # merge only non-null fields
        for key, value in parsed.items():
            if value:
                data[key] = value

        data["user_answers"] = answer
        data = normalize_empty(data)

    return {
        "goal_data": data
    }