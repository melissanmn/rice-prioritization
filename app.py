import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Prioritize", layout="centered")

# INTER + SPACING
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    .stApp {background: #FFFFFF; padding: 1rem;}
    .stTextArea > div > div > textarea {border-radius: 12px; border: 1px solid #D1D5DB; padding: 12px;}
    .stExpander {border-radius: 12px; border: 1px solid #E5E7EB; margin: 16px 0; background: #FAFBFC;}
    .stExpander > div > div {padding: 20px !important;}
    .stRadio {margin: 24px 0;}
    .slider-row {padding: 8px 0;}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("Prioritize")
st.caption("Rank your product ideas in seconds")

# INPUT
ideas = st.text_area(
    "Your ideas (one per line)",
    "Add dark mode\nFix login bug\nBuild AI summary",
    height=120
).strip().split("\n")
ideas = [i.strip() for i in ideas if i.strip()]

if ideas:
    mode = st.radio("Framework", ["RICE", "ICE"], horizontal=True)

    data = []
    for i, idea in enumerate(ideas):
        with st.expander(f"**{idea}**", expanded=i == 0):
            # Init session state
            for param, default in zip(["r", "i", "c", "e"], [100, 1, 80, 5]):
                key = f"{param}{i}"
                if key not in st.session_state:
                    st.session_state[key] = default

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="slider-row">', unsafe_allow_html=True)
                reach = st.slider("Reach (users)", 0, 1000, st.session_state[f"r{i}"])
                impact = st.slider("Impact (0–3)", 0, 3, st.session_state[f"i{i}"])
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="slider-row">', unsafe_allow_html=True)
                confidence = st
