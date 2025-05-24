# auth/login.py
import pandas as pd
import streamlit as st
def load_users():
    return pd.read_csv("data/users.csv")
def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        users = load_users()
        user = users[(users['username'] == username) & (users['password'] == password)]
        if not user.empty:
            st.session_state["user"] = {
                "username": username,
                "role": user.iloc[0]['role']
            }
            st.sidebar.success(f"Welcome {username}!")
        else:
            st.sidebar.error("Invalid username or password")

def get_current_user():
    return st.session_state.get("user", None)
