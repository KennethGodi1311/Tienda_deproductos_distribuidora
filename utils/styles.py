import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    .stApp {
        background: #020617;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)