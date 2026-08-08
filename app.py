# GitHub Repository:
# git add  .
# git commit -m "Initial commit"
# git push origin main

#Streamlit Commands:
# streamlit run app.py

import streamlit as st

st.title("Blinkit Price predictor")

name = st.text_input("product name:")
weight = st.text_input("weight:")
rating = st.text_input("rating:",1,5)
category = st.selectbox(
    "category:",
    ["Milk", "Snacks", "Fruits"]
)

if st.button("Predict Price"):
    st.success("Prediction Complete")
