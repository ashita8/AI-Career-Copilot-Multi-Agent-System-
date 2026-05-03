# ==========================================================
# app/agents/general_chat_agent.py
# UPDATED GENERAL CHAT + LIGHT ORCHESTRATOR
# Routes to specialized agents when needed,
# otherwise handles normal conversation.
# ==========================================================

from datetime import datetime
from typing import Dict, Any

from services.groq_client import llm

# Specialized Agents
from agents.goal_agent import goal_agent
from agents.skill_gap_agent import skill_gap_agent
from agents.roadmap_agent import roadmap_agent
from agents.project_agent import project_agent
from agents.resume_agent import resume_agent


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are Career Copilot AI.

You are an elite AI career strategist and assistant.

Your job:

1. Help users grow careers in tech.
2. Be practical, modern, concise.
3. Give strong advice.
4. Ask smart follow-up questions when needed.
5. Use known user context.
6. Never mention internal tools.
"""


# ==========================================================
# CONTEXT BUILDER
# ==========================================================

def build_context(state: Dict[str, Any]) -> str:

    context = []

    if state.get("goal_data"):
        context.append(f"Goal: {state['goal_data']}")

    if state.get("skill_gap_data"):
        context.append(f"Skill Gap: {state['skill_gap_data']}")

    if state.get("roadmap_data"):
        context.append(f"Roadmap: {state['roadmap_data']}")

    if state.get("project_data"):
        context.append(f"Projects: {state['project_data']}")

    if state.get("resume_data"):
        context.append(f"Resume: {state['resume_data']}")

    print("context",context)
    return "\n".join(context)


# ==========================================================
# LIGHT INTENT ROUTER
# ==========================================================

def detect_intent(message: str, state: Dict[str, Any]) -> str:

    msg = message.lower().strip()

    if state.get("resume_text", "").strip():
        return "resume"

    if any(word in msg for word in ["resume", "cv", "ats"]):
        return "resume"

    if any(word in msg for word in ["project", "portfolio"]):
        return "project"

    if any(word in msg for word in ["roadmap", "study plan", "learning plan"]):
        return "roadmap"

    if any(word in msg for word in ["skill gap", "missing skills", "what should i learn"]):
        return "skill_gap"

    if any(word in msg for word in ["become", "career switch", "transition", "goal"]):
        return "goal"

    return "chat"


# ==========================================================
# MAIN AGENT
# ==========================================================

def general_chat_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Smart entrypoint:
    - Detect intent
    - Route to right agent
    - Else chat normally
    """

    try:
        user_message = state.get("message", "").strip()

        if not user_message and not state.get("resume_text"):
            return {
                "general_chat_data": {
                    "reply": "How can I help you today?"
                }
            }

        # --------------------------------------------------
        # Detect intent
        # --------------------------------------------------
        intent = detect_intent(user_message, state)

        # --------------------------------------------------
        # Route to agents
        # --------------------------------------------------
        if intent == "resume":
            return resume_agent(state)

        if intent == "goal":
            return goal_agent(state)

        if intent == "skill_gap":
            return skill_gap_agent(state)

        if intent == "roadmap":
            return roadmap_agent(state)

        if intent == "project":
            return project_agent(state)

        # --------------------------------------------------
        # Normal Chat Mode
        # --------------------------------------------------
        context = build_context(state)

        prompt = f"""
        {SYSTEM_PROMPT}

        DATE:
        {datetime.utcnow().strftime("%Y-%m-%d")}

        KNOWN CONTEXT:
        {context}

        USER MESSAGE:
        {user_message}

        Reply naturally and helpfully.
        """

        result = llm.invoke(prompt)

        content = getattr(result, "content", str(result)).strip()

        return {
            "general_chat_data": {
                "reply": content
            }
        }

    except Exception:
        return {
            "general_chat_data": {
                "reply": "Something went wrong. Please try again."
            }
        }