from langgraph.graph import StateGraph, START, END
from app.schemas.user_feedback_state import UserFeedbackState
from app.graph.user_feedback_nodes import user_feedback_research_agent
from sqlalchemy.orm import Session
from app.db.checkpointer import checkpointer

graph = StateGraph(UserFeedbackState)
    

    
graph.add_node("user_feedback_research_agent", user_feedback_research_agent)

graph.add_edge(START, "user_feedback_research_agent")
graph.add_edge("user_feedback_research_agent", END)
    
UserFeedbackGraph = graph.compile()	