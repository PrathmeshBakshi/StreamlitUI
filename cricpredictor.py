"""
Cricket Run Predictor - Streamlit App
--------------------------------------
Predicts the projected/final score of a cricket innings based on the
current match situation (overs bowled, current score, wickets fallen,
recent run rate, etc.) using a simple regression model.

Run with:
    streamlit cricpredictor.py

Dependencies:
    pip install streamlit scikit-learn numpy pandas
"""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(page_title="Cricket Run Predictor", page_icon="🏏", layout="centered")

# --------------------------------------------------------------------------
# Synthetic training data + model
# --------------------------------------------------------------------------
# In a real project you'd load historical ball-by-ball / innings data (e.g.
# from Cricsheet or an IPL dataset) instead of generating synthetic data.
@st.cache_resource
def train_model(match_format: str):
    rng = np.random.default_rng(42)
    n_samples = 5000

    total_overs = 20 if match_format == "T20" else 50

    overs_completed = rng.uniform(5, total_overs, n_samples)
    current_run_rate = rng.uniform(4, 11, n_samples)
    wickets_fallen = rng.integers(0, 8, n_samples)
    last_5_over_runs = rng.uniform(15, 70, n_samples)

    current_score = overs_completed * current_run_rate

    # Synthetic "ground truth" final score with some realistic logic:
    # higher recent run rate + fewer wickets lost + more overs left -> higher final score
    overs_left = total_overs - overs_completed
    wicket_penalty = wickets_fallen * 1.5
    momentum = (last_5_over_runs / 5) * 0.6

    final_score = (
        current_score
        + overs_left * (current_run_rate * 0.9 + momentum * 0.3)
        - wicket_penalty * overs_left * 0.15
        + rng.normal(0, 5, n_samples)  # noise
    )
    final_score = np.clip(final_score, current_score, None)

    X = pd.DataFrame({
        "overs_completed": overs_completed,
        "current_score": current_score,
        "wickets_fallen": wickets_fallen,
        "current_run_rate": current_run_rate,
        "last_5_over_runs": last_5_over_runs,
        "overs_left": overs_left,
    })
    y = final_score

    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_final_score(model, overs_completed, current_score, wickets_fallen,
                         current_run_rate, last_5_over_runs, total_overs):
    overs_left = total_overs - overs_completed
    X_new = pd.DataFrame([{
        "overs_completed": overs_completed,
        "current_score": current_score,
        "wickets_fallen": wickets_fallen,
        "current_run_rate": current_run_rate,
        "last_5_over_runs": last_5_over_runs,
        "overs_left": overs_left,
    }])
    prediction = model.predict(X_new)[0]
    return max(prediction, current_score)  # score can't decrease


# --------------------------------------------------------------------------
# UI
# --------------------------------------------------------------------------
st.title("🏏 Cricket Run Predictor")
st.write(
    "Estimate a team's projected final innings score based on the current "
    "match situation. This demo model is trained on **synthetic data** — "
    "swap in a real dataset (e.g. Cricsheet / IPL ball-by-ball data) for "
    "production use."
)

match_format = st.radio("Match format", ["T20", "ODI"], horizontal=True)
total_overs = 20 if match_format == "T20" else 50

col1, col2 = st.columns(2)
with col1:
    overs_completed = st.slider(
        "Overs completed", min_value=1.0, max_value=float(total_overs - 1),
        value=float(total_overs) / 2, step=0.1,
    )
    wickets_fallen = st.slider("Wickets fallen", 0, 9, 3)

with col2:
    current_score = st.number_input(
        "Current score (runs)", min_value=0,
        value=int(overs_completed * 7), step=1,
    )
    last_5_over_runs = st.slider(
        "Runs scored in last 5 overs", 0, 100, 35,
        help="Use fewer overs' worth of runs if less than 5 overs have been bowled.",
    )

current_run_rate = current_score / overs_completed if overs_completed > 0 else 0.0
st.metric("Current Run Rate", f"{current_run_rate:.2f}")

st.divider()

if st.button("🔮 Predict Final Score", type="primary", use_container_width=True):
    model = train_model(match_format)
    prediction = predict_final_score(
        model,
        overs_completed=overs_completed,
        current_score=current_score,
        wickets_fallen=wickets_fallen,
        current_run_rate=current_run_rate,
        last_5_over_runs=last_5_over_runs,
        total_overs=total_overs,
    )

    st.success(f"### Projected final score: **{prediction:.0f} runs**")

    remaining_overs = total_overs - overs_completed
    required_rate_for_prediction = (
        (prediction - current_score) / remaining_overs if remaining_overs > 0 else 0
    )
    st.write(
        f"Projected run rate needed for the rest of the innings: "
        f"**{required_rate_for_prediction:.2f} runs/over**"
    )

st.caption(
    "⚠️ This is a simplified demo model for illustration purposes and does "
    "not account for pitch conditions, bowling quality, venue, or opposition "
    "strength. Do not use for betting or real-money decisions."
)