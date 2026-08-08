# git add  .
# git commit -m "Initial commit"
# git push origin main
# streamlit run app.py

import streamlit as st

st.title("My Website")
st.subheader("This website is used for machine learning")
st.markdown("Just going for **SQL**")

st.write("This is a normal text")

if st.button("Click me"):
    st.write("Working on prediction.....")

if st.button("View Chart"):
    st.write("Bar Plot is Here")

name = st.text_input("Enter your name")
st.write(name)

age = st.number_input("Enter your age")
st.write(age)

rating = st.slider("Rate your experience", 0, 10)
st.write(rating)