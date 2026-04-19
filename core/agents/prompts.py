# core/agents/prompts.py

from langchain_core.prompts import ChatPromptTemplate

RETENTION_PLAN_SYSTEM_PROMPT = """
You are an Expert Game Economy and Engagement Designer. 
Your job is to create retention plans for players at risk of churning. 
You must base your recommendations strictly on the provided 'Retrieved Strategies'.
"""

RETENTION_PLAN_HUMAN_PROMPT = """
Player Profile: {player_data}
Churn Risk: {churn_probability}
Identified Risks: {risk_factors}

Retrieved Strategies from Playbook:
{retrieved_strategies}

Generate a structured retention plan based on these exact details.
"""

def get_retention_plan_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", RETENTION_PLAN_SYSTEM_PROMPT),
        ("human", RETENTION_PLAN_HUMAN_PROMPT)
    ])
