from app.services.llm import get_openai_llm
from app.schemas.user_feedback_state import UserFeedbackState
from app.prompts.user_feedback import UserFeedbackResearchAgentPrompt
from openai import OpenAI


def user_feedback_research_agent(state: UserFeedbackState) -> UserFeedbackState:

    """Fetches chat history, generates the acquisition strategy via LLM."""


    prompt = UserFeedbackResearchAgentPrompt.format(
        feedback_transcripts=state.feedback_transcripts,
        support_logs=state.support_logs,
        nps_data=state.nps_data
    )

    client = OpenAI()

    resp = client.responses.create(
        model="gpt-4.1",    
        input=prompt,
        tools=[{"type": "web_search"}],
        temperature=0.0
    )

    assistant_call = next(item for item in resp.output if item.type == "message")
    state.response = assistant_call.content[0].text

    return state
