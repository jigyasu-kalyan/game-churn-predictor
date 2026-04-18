import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables (API Keys)
load_dotenv()

# Import the compiled LangGraph workflow
from graph import app_graph

# --- UI Configuration ---
st.set_page_config(page_title="Agentic Retention Optimizer", page_icon="🎮", layout="wide")

st.title("🎮 Agentic Player Retention Optimizer")
st.markdown("Enter player metrics below to trigger the AI agent for churn analysis and personalized retention planning.")

# --- Sidebar Inputs (From Milestone 1) ---
st.sidebar.header("Player Data Inputs")

age = st.sidebar.slider("Age", min_value=10, max_value=100, value=25)
playtime = st.sidebar.slider("Playtime (Hours)", min_value=0.0, max_value=500.0, value=20.0)
purchases = st.sidebar.slider("In-Game Purchases ($)", min_value=0.0, max_value=5000.0, value=0.0) # Default changed to 0 to test churn
sessions = st.sidebar.slider("Sessions per week", min_value=0, max_value=50, value=2) # Default changed to 2 to test churn
duration = st.sidebar.slider("Avg session duration (mins)", min_value=0, max_value=300, value=25)
level = st.sidebar.slider("Player level", min_value=1, max_value=100, value=10)
achievements = st.sidebar.slider("Achievements unlocked", min_value=0, max_value=1000, value=5)

gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
location = st.sidebar.selectbox("Location", ["USA", "Europe", "Asia", "Other"])
genre = st.sidebar.selectbox("Genre", ["Action", "RPG", "Strategy", "Sports"])
difficulty = st.sidebar.selectbox("Game Difficulty", ["Easy", "Medium", "Hard"], index=2) # Default Hard

# --- Execution Logic ---
if st.button("Generate Agentic Retention Plan", type="primary", use_container_width=True):
    
    # Check for API Key before running
    if not os.environ.get("GROQ_API_KEY"):
        st.error("🚨 API Key Missing! Please set your GROQ_API_KEY in the .env file or Streamlit Secrets.")
        st.stop()

    input_data = {
        'Age': age, 'PlayTimeHours': playtime, 'InGamePurchases': purchases,
        'SessionsPerWeek': sessions, 'AvgSessionDurationMinutes': duration,
        'PlayerLevel': level, 'AchievementsUnlocked': achievements,
        'Gender': gender, 'Location': location,
        'GameGenre': genre, 'GameDifficulty': difficulty
    }

    st.divider()
    
    with st.spinner("🤖 Agent is analyzing player behavior and retrieving strategies..."):
        try:
            # 1. Invoke the LangGraph workflow
            final_state = app_graph.invoke({"player_data": input_data})
            
            # 2. Extract Data
            churn_prob = final_state["churn_probability"]
            churn_class = final_state["churn_class"]
            plan = final_state["final_plan"]
            
            # --- Presentation Layer ---
            
            # Top Row: Risk Metrics
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                if churn_class == 1:
                    st.error("🚨 HIGH CHURN RISK DETECTED")
                else:
                    st.success("✅ RETAINED (LOW RISK)")
            with metric_col2:
                st.metric(label="Churn Probability", value=f"{churn_prob*100:.1f}%")
                st.progress(float(churn_prob))
            
            st.markdown("### 📋 Agentic Retention Plan")
            
            # Structured Output Layout
            st.info(f"**Behavioral Summary:**\n\n{plan['summary']}")
            
            if churn_class == 1:
                st.warning(f"**Risk Analysis:**\n\n{plan['analysis']}")
            
            st.success(f"**Recommended Intervention Plan:**\n\n{plan['plan']}")
            
            # Accordion for less critical info (References & Disclaimers)
            with st.expander("📚 View Strategy Context & References"):
                st.write(plan['refs'])
            
            st.caption(f"**Ethical & UX Disclaimer:** {plan['disclaimer']}")

        except Exception as e:
            st.error(f"An error occurred during workflow execution: {e}")
            st.info("System gracefully degraded. Please check logs.")