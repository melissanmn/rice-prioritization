import streamlit as st
import pandas as pd
import plotly.express as px

# LIGHT MODE + MODERN
st.set_page_config(page_title="Prioritize", layout="centered")
st.markdown("""
<style>
    .big-font {font-size: 42px !important; font-weight: 800; color: #1E1E1E;}
    .subtitle {font-size: 18px; color: #555; margin-bottom: 30px;}
    .stRadio > div {flex-direction: row; gap: 20px;}
    .stExpander {border: 1px solid #E5E7EB; border-radius: 12px; margin: 8px 0;}
    .stSlider > div > div {background: #F3F4F6;}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<p class="big-font">Prioritize</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Rank your product ideas in 60 seconds</p>', unsafe_allow_html=True)

# INPUT
ideas = st.text_area(
    "Your ideas (one per line)",
    "Add dark mode\nFix login bug\nBuild AI summary",
    height=120,
    help="Paste or type — we’ll rank them instantly"
).split("\n")
ideas = [i.strip() for i in ideas if i.strip()]

if ideas:
    mode = st.radio("Framework", ["RICE", "ICE"], horizontal=True)
    data = []

    for i, idea in enumerate(ideas):
        with st.expander(f"**{idea}**", expanded=True):
            c1, c2 = st.columns(2)
            reach = c1.slider("Reach (users in 3mo)", 0, 1000, 100, key=f"r{i}")
            impact = c1.slider("Impact (0=low, 3=high)", 0, 3, 1, key=f"i{i}")
            confidence = c2.slider("Confidence %", 0, 100, 80, key=f"c{i}")
            effort = c2.slider("Effort (person-days)", 1, 30, 5, key=f"e{i}")

            score = (reach * impact * confidence / 100) / effort if mode == "RICE" else \
                    (impact * confidence * (100 - effort/30*100)) / 10000

            data.append({"Idea": idea, "Score": round(score, 1), "Effort": effort})

    df = pd.DataFrame(data).sort_values("Score", ascending=False)
    
st.success(f"### Top Idea: **{df.iloc[0]['Idea']}** ({mode}: {df.iloc[0]['Score']})")
