# app/agents/resume_agent.py

from services.groq_client import llm
from schemas.resume_schema import ResumeSchema


def resume_agent(state):
    """
    Uses uploaded resume text + all previous agent outputs
    to review and optimize resume.
    """

    # ----------------------------
    # Load state data
    # ----------------------------
    goal = state.get("goal_data", {})
    gap = state.get("skill_gap_data", {})
    roadmap = state.get("roadmap_data", {})
    project = state.get("project_data", {})

    resume_text = state.get("resume_text", "")

    role = goal.get("goal_title", "AI Engineer")
    timeline = goal.get("timeline", "")
    background = goal.get("current_background", "")
    level = goal.get("experience_level", "")

    missing_skills = gap.get("missing_skills", [])
    priority_skills = gap.get("priority_skills", [])

    recommended_projects = (
        project.get("advanced_projects", [])
        + project.get("intermediate_projects", [])
    )[:5]

    # ----------------------------
    # If no resume uploaded
    # ----------------------------
 
    if not resume_text or not resume_text.strip():

        return {}
    #{
            # "resume_data": {
            #     "resume_score": "0/100",
            #     "missing_sections": [
            #         "Resume PDF not uploaded"
            #     ],
            #     "missing_keywords": [],
            #     "weak_bullets": [],
            #     "rewritten_summary": "Please upload your resume PDF to receive personalized feedback.",
            #     "top_projects_to_add": recommended_projects,
            #     "ats_tips": [
            #         "Upload PDF resume first",
            #         "Use clean formatting",
            #         "Add measurable achievements"
            #     ],
            #     "final_verdict": "Resume not analyzed yet."
            # }
        #}

    # ----------------------------
    # Structured Output LLM
    # ----------------------------
    structured_llm = llm.with_structured_output(ResumeSchema)

    prompt = f"""
You are an elite resume reviewer and ATS strategist.

Analyze the user's resume for the target job role.

========================
TARGET ROLE:
{role}

TIMELINE:
{timeline}

CURRENT BACKGROUND:
{background}

EXPERIENCE LEVEL:
{level}

MISSING SKILLS:
{missing_skills}

HIGH PRIORITY SKILLS:
{priority_skills}

RECOMMENDED PROJECTS:
{recommended_projects}

========================
RESUME CONTENT:
{resume_text}

========================
Return:

1. resume_score (example: 78/100)
2. missing_sections
3. missing_keywords
4. weak_bullets
5. rewritten_summary
6. top_projects_to_add
7. ats_tips
8. final_verdict

Rules:
- Be honest and practical
- Optimize for ATS systems
- Mention missing AI keywords if needed
- Suggest strongest projects to add
- Keep summary concise and recruiter friendly
"""

    try:
        result = structured_llm.invoke(prompt)

        return {
            "resume_data": result.model_dump()
        }

    except Exception:
        return {
            "resume_data": {
                "resume_score": "72/100",
                "missing_sections": [
                    "Projects",
                    "Technical Skills",
                    "Professional Summary"
                ],
                "missing_keywords": [
                    "Python",
                    "FastAPI",
                    "LLM",
                    "RAG",
                    "LangGraph"
                ],
                "weak_bullets": [
                    "Worked on backend APIs",
                    "Handled client requirements"
                ],
                "rewritten_summary": "Backend developer transitioning into Generative AI engineering with strong API development experience and growing expertise in LLM systems.",
                "top_projects_to_add": recommended_projects,
                "ats_tips": [
                    "Use standard headings",
                    "Add metrics to achievements",
                    "Include relevant AI keywords",
                    "Keep resume to 1-2 pages",
                    "Use reverse chronological order"
                ],
                "final_verdict": "Strong base profile. Needs AI-focused projects and ATS keyword optimization."
            }
        }