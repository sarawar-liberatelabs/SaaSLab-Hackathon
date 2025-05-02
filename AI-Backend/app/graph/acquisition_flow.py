from langgraph.graph import StateGraph, START, END
from app.schemas.acquisition_state import AcquisitionState
from app.graph.acquisition_nodes import acquisition_strategy
from sqlalchemy.orm import Session
from app.db.checkpointer import checkpointer

graph = StateGraph(AcquisitionState)
    

    
graph.add_node("acquisition_strategy", acquisition_strategy)

graph.add_edge(START, "acquisition_strategy")
graph.add_edge("acquisition_strategy", END)
    
AcquisitionGraph = graph.compile(checkpointer=checkpointer)