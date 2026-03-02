# 🎮 Project: Player Churn Prediction & Agentic Retention Strategy

## From Predictive Analytics to Intelligent Intervention

### Project Overview
This project involves the design and implementation of an **AI-driven player analytics system** that predicts churn in gaming environments and will evolve into an agentic AI retention strategist for the final submission.

- **Milestone 1 (Current):** Classical machine learning (Random Forest) applied to historical player behavior data to predict churn risk and identify key drivers of disengagement.
- **Milestone 2 (Upcoming):** Extension into an agent-based AI application using LangGraph to autonomously reason about churn risk and plan intervention strategies.

---

### Technology Stack (Milestone 1)
| Component | Technology |
| :--- | :--- |
| **ML Models** | Random Forest, Logistic Regression, Scikit-Learn |
| **Data Processing** | Pandas, NumPy, StandardScaler, OneHotEncoder |
| **UI Framework** | Streamlit |
| **Environment** | Python 3.11+, Virtualenv |

---

### Milestone 1 Deliverables (Mid-Sem)

#### 1. Problem Understanding & Business Context
**Objective:** Identify players at risk of leaving the game using behavioral data (PlayTime, Sessions, Purchases). 
**Context:** High churn rates directly impact game revenue. By predicting "Low Engagement" players early, developers can trigger retention rewards or difficulty adjustments to keep the player base active.

#### 2. System Architecture
The system utilizes a **Scikit-Learn Pipeline** for seamless data flow:
1. **Input:** Raw player metrics via Streamlit UI.
2. **Preprocessing:** Automated scaling of numbers and encoding of categories.
3. **Inference:** A saved Random Forest model (`.pkl`) generates a probability score.
4. **Output:** Real-time risk classification and probability display.

#### 3. Model Performance Evaluation
We compared a baseline Logistic Regression model against a Random Forest Classifier.

| Metric | Logistic Regression | Random Forest (Final) |
| :--- | :--- | :--- |
| **Accuracy** | 82.4% | **93.9%** |
| **Precision** | 61.9% | **90.8%** |
| **Recall** | 85.0% | **85.3%** |
| **AUC Score** | 0.832 | **0.911%** |

---

### How to Run Locally
1. Clone the repo: `git clone https://github.com/jigyasu-kalyan/game-churn-predictor`
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

### 🌐 Live Deployment
**Hosted Link:** https://game-churn-predictor.streamlit.app/