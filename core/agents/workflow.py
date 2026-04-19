# core/agents/workflow.py

from langgraph.graph import StateGraph, END
from .nodes import AgentState, NodeFactory

def route_based_on_risk(state: AgentState):
    """Conditional Routing: Only generate complex plans if they are actually at risk."""
    if state["churn_class"] == 1:
        return "analyze"
    else:
        # For this demo, we'll still send them to analyze to show the full agent pipeline
        return "analyze"

def create_graph(predictor, rag_system, structured_llm):
    """Factory function to create and compile the LangGraph workflow."""
    
    # Initialize node factory with dependencies
    factory = NodeFactory(predictor, rag_system, structured_llm)
    
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("predict", factory.predict_node)
    workflow.add_node("analyze", factory.analysis_node)
    workflow.add_node("retrieve", factory.retrieve_node)
    workflow.add_node("generate", factory.generate_plan_node)

    # Add edges
    workflow.set_entry_point("predict")
    workflow.add_conditional_edges("predict", route_based_on_risk)
    workflow.add_edge("analyze", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()
