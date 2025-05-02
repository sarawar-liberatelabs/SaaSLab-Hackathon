from app.curd.chat_history import get_chat_history, ChatHistoryRequest
from app.schemas.chat_history import ChatHistoryResponse
from app.prompts.acquisition import ACQUISITION_STRATEGY_AGENT_PROMPT
from app.schemas.acquisition_state import AcquisitionState
from fastapi import Depends
from app.db.database import get_db
from openai import OpenAI

def acquisition_strategy(state: AcquisitionState) -> AcquisitionState:
    """Fetches chat history, generates the acquisition strategy via LLM with live web access."""
    # db = get_db()

    # # 2. Load past chat history
    # chat_history = ChatHistoryResponse(
    #     chat_history=get_chat_history(
    #         ChatHistoryRequest(thread_id=int(state.thread_id)),
    #         db=db
    #     )
    # )

    prompt = ACQUISITION_STRATEGY_AGENT_PROMPT.format(
        input=state.message
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
