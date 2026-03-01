import streamlit as st
import pandas as pd
import joblib

# Loading the trained pipeline
@st.cache_resource
def load_model():
    return joblib.load('churn_model.pkl')

pipeline = load_model()

# UI Layout
st.title("🎮 Player Churn Predictor")
st.markdown("Enter player metrics below to evaluate player retention risk.")

st.sidebar.header("Player Data Inputs")

# Numeric Features
age = st.sidebar.slider("Age", min_value=10, max_value=100, value=25)
playtime = st.sidebar.slider("Playtime (Hours)", min_value=0.0, max_value=500.0, value=20.0)
purchases = st.sidebar.slider("In-Game Purchases ($)", min_value=0.0, max_value=5000.0, value=15.0)
sessions = st.sidebar.slider("Sessions per week", min_value=0, max_value=50, value=5)
duration = st.sidebar.slider("Avg session duration (mins)", min_value=0, max_value=300, value=45)
level = st.sidebar.slider("Player level", min_value=1, max_value=100, value=10)
achievements = st.sidebar.slider("Achievements unlocked", min_value=0, max_value=1000, value=20)

# Categorical Features
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
location = st.sidebar.selectbox("Location", ["USA", "Europe", "Asia", "Other"])
genre = st.sidebar.selectbox("Genre", ["Action", "RPG", "Strategy", "Sports"])
difficulty = st.sidebar.selectbox("Game Difficulty", ["Easy", "Medium", "Hard"])

# Prediction Logic
if st.button("Predict Churn Risk", type="primary"):
    # Structuring inputs into a DataFrame from the model
    input_data = pd.DataFrame({
        'Age': [age],
        'PlayTimeHours': [playtime],
        'InGamePurchases': [purchases],
        'SessionsPerWeek': [sessions],
        'AvgSessionDurationMinutes': [duration],
        'PlayerLevel': [level],
        'AchievementsUnlocked': [achievements],
        'Gender': [gender],
        'Location': [location],
        'GameGenre': [genre],
        'GameDifficulty': [difficulty]
    })

    # Making predictions
    churn_prob = pipeline.predict_proba(input_data)[0][1]
    churn_class = pipeline.predict(input_data)[0]

    st.divider()

    # Displaying results
    col1, col2 = st.columns(2)
    with col1:
        if churn_class == 1:
            st.error("🚨 HIGH RISK: Player is likely to churn")
        else:
            st.success("✅ LOW RISK: Player is likely to retain")
    with col2:
        st.metric(label="Churn Probability", value=f"{churn_prob*100:.1f}%")
        st.progress(float(churn_prob))