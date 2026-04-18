import os
import pandas as pd
import joblib
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Import your custom RAG module
from rag import EngagementRAG

# --- 1. Define the Structured Output (Rubric Requirement) ---
class RetentionPlan(BaseModel):
    """Strictly enforces the 5-part output structure required by the rubric."""
    summary: str = Field(description="Player Behavior Overview based on their data.")
    analysis: str = Field(description="Churn Risk Interpretation. Why are they at risk?")
    plan: str = Field(description="Engagement & Retention Recommendations based on the strategies.")
    refs: str = Field(description="Supporting References from the provided strategy context.")
    disclaimer: str = Field(description="Ethical & UX Disclaimers regarding the intervention.")

# --- 2. Define the Graph State ---
class AgentState(TypedDict):
    player_data: dict
    churn_probability: float
    churn_class: int
    risk_factors: List[str]
    retrieved_strategies: str
    final_plan: Dict[str, Any]

# --- 3. Initialize Global Components ---
# NOTE: Set your GROQ_API_KEY in your environment variables (.env file)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
structured_llm = llm.with_structured_output(RetentionPlan)
rag_system = EngagementRAG()

try:
    ml_pipeline = joblib.load('churn_model.pkl')
except FileNotFoundError:
    print("WARNING: churn_model.pkl not found. Graph will fail at prediction node.")
    ml_pipeline = None

# --- 4. Define the Nodes ---

def predict_node(state: AgentState):
    """Runs the tabular player data through the Random Forest model."""
    print("--- NODE: Predicting Churn Risk ---")
    df = pd.DataFrame([state["player_data"]])
    
    # Predict
    prob = ml_pipeline.predict_proba(df)[0][1]
    predicted_class = ml_pipeline.predict(df)[0]
    
    return {"churn_probability": prob, "churn_class": int(predicted_class)}

def analysis_node(state: AgentState):
    """Rule-based extraction of risk factors based on the player's metrics."""
    print("--- NODE: Analyzing Risk Factors ---")
    data = state["player_data"]
    risk_factors = []
    
    # Identify pain points (You can adjust these thresholds based on your EDA)
    if data.get("GameDifficulty") == "Hard" and data.get("AvgSessionDurationMinutes", 100) < 30:
        risk_factors.append("Frustration/Rage-quitting due to high difficulty and short sessions.")
    if data.get("SessionsPerWeek", 5) <= 2:
        risk_factors.append("Declining session frequency; risk of habit breaking.")
    if data.get("PlayerLevel", 0) > 50 and data.get("SessionsPerWeek", 5) < 3:
        risk_factors.append("Veteran player content exhaustion.")
    if len(risk_factors) == 0:
        risk_factors.append("General engagement drop.")
        
    return {"risk_factors": risk_factors}

def retrieve_node(state: AgentState):
    """Queries ChromaDB using the identified risk factors."""
    print("--- NODE: Retrieving Strategies ---")
    context = rag_system.retrieve_strategies(state["risk_factors"])
    return {"retrieved_strategies": context}

def generate_plan_node(state: AgentState):
    """Uses the LLM to generate the final 5-part plan based on context."""
    print("--- NODE: Generating Final Plan ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Expert Game Economy and Engagement Designer. Your job is to create retention plans for players at risk of churning. You must base your recommendations strictly on the provided 'Retrieved Strategies'."),
        ("human", """
        Player Profile: {player_data}
        Churn Risk: {churn_probability}
        Identified Risks: {risk_factors}
        
        Retrieved Strategies from Playbook:
        {retrieved_strategies}
        
        Generate a structured retention plan based on these exact details.
        """)
    ])
    
    chain = prompt | structured_llm
    
    try:
        # Generate the structured response
        response = chain.invoke({
            "player_data": state["player_data"],
            "churn_probability": f"{state['churn_probability']:.2%}",
            "risk_factors": ", ".join(state["risk_factors"]),
            "retrieved_strategies": state["retrieved_strategies"]
        })
        # Convert pydantic object to dictionary for the state
        plan_dict = response.dict()
    except Exception as e:
        print(f"LLM Generation Error: {e}")
        # Graceful Fallback (Rubric requirement)
        plan_dict = {
            "summary": "System encountered an error parsing player data.",
            "analysis": "Unable to complete deep analysis.",
            "plan": "Standard Fallback: Offer a 10% XP boost for the next 24 hours.",
            "refs": "Fallback System Triggered.",
            "disclaimer": "Automated fallback response. No ethical concerns."
        }
        
    return {"final_plan": plan_dict}

# --- 5. Build and Compile the Graph ---

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("predict", predict_node)
workflow.add_node("analyze", analysis_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_plan_node)

# Add edges (Linear flow for high-risk players)
workflow.set_entry_point("predict")

# Conditional Routing: Only generate complex plans if they are actually at risk
def route_based_on_risk(state: AgentState):
    if state["churn_class"] == 1:
        return "analyze"
    else:
        # If low risk, we could route to END, but let's just generate a 'maintenance' plan
        # We'll still send them to analyze, but the LLM will see a low churn probability.
        return "analyze"

workflow.add_conditional_edges("predict", route_based_on_risk)
workflow.add_edge("analyze", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

# Compile
app_graph = workflow.compile()

# --- Testing Block ---
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Make sure to have a .env file with GROQ_API_KEY=your_key
    
    test_player = {
        'Age': 25, 'PlayTimeHours': 12.5, 'InGamePurchases': 0, 
        'SessionsPerWeek': 2, 'AvgSessionDurationMinutes': 25, 
        'PlayerLevel': 15, 'AchievementsUnlocked': 5, 
        'Gender': 'Female', 'Location': 'USA', 
        'GameGenre': 'Action', 'GameDifficulty': 'Hard'
    }
    
    print("\nInvoking Agentic Workflow...\n")
    final_state = app_graph.invoke({"player_data": test_player})
    
    print("\n=== FINAL STRUCTURED OUTPUT ===")
    for key, value in final_state["final_plan"].items():
        print(f"\n[{key.upper()}]\n{value}")