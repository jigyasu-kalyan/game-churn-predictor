# core/agents/nodes.py

import pandas as pd
from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field
from .prompts import get_retention_plan_prompt
from ..utils.logger import logger

# --- 1. Define the Structured Output ---
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

# --- 3. Node Factory Wrapper ---
class NodeFactory:
    def __init__(self, predictor, rag_system, structured_llm):
        self.predictor = predictor
        self.rag_system = rag_system
        self.structured_llm = structured_llm

    def predict_node(self, state: AgentState):
        """Runs the tabular player data through the ML model."""
        logger.info("NODE: Predicting Churn Risk")
        prob, predicted_class = self.predictor.predict(state["player_data"])
        return {"churn_probability": prob, "churn_class": predicted_class}

    def analysis_node(self, state: AgentState):
        """Rule-based extraction of risk factors based on the player's metrics."""
        logger.info("NODE: Analyzing Risk Factors")
        data = state["player_data"]
        risk_factors = []
        
        # Identify pain points
        if data.get("GameDifficulty") == "Hard" and data.get("AvgSessionDurationMinutes", 100) < 30:
            risk_factors.append("Frustration/Rage-quitting due to high difficulty and short sessions.")
        if data.get("SessionsPerWeek", 5) <= 2:
            risk_factors.append("Declining session frequency; risk of habit breaking.")
        if data.get("PlayerLevel", 0) > 50 and data.get("SessionsPerWeek", 5) < 3:
            risk_factors.append("Veteran player content exhaustion.")
        if not risk_factors:
            risk_factors.append("General engagement drop.")
            
        return {"risk_factors": risk_factors}

    def retrieve_node(self, state: AgentState):
        """Queries ChromaDB using the identified risk factors."""
        logger.info("NODE: Retrieving Strategies")
        context = self.rag_system.retrieve_strategies(state["risk_factors"])
        return {"retrieved_strategies": context}

    def generate_plan_node(self, state: AgentState):
        """Uses the LLM to generate the final 5-part plan based on context."""
        logger.info("NODE: Generating Final Plan")
        
        prompt = get_retention_plan_prompt()
        chain = prompt | self.structured_llm
        
        try:
            response = chain.invoke({
                "player_data": state["player_data"],
                "churn_probability": f"{state['churn_probability']:.2%}",
                "risk_factors": ", ".join(state["risk_factors"]),
                "retrieved_strategies": state["retrieved_strategies"]
            })
            plan_dict = response.dict()
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            plan_dict = {
                "summary": "System encountered an error parsing player data.",
                "analysis": "Unable to complete deep analysis.",
                "plan": "Standard Fallback: Offer a 10% XP boost for the next 24 hours.",
                "refs": "Fallback System Triggered.",
                "disclaimer": "Automated fallback response. No ethical concerns."
            }
            
        return {"final_plan": plan_dict}
