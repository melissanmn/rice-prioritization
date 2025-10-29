import streamlit as st
import pandas as pd
import plotly.express as px

# FORCE LIGHT + MODERN FONT + FIX ALL TEXT
st.set_page_config(page_title="Prioritize", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"], .stApp, textarea, input, select, button, label, p, div, span, h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    .stTextArea > div > div > textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }
    .stExpander > div > label {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    .stExpander {
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }
    .stRadio > div > label {
        color: #000000 !important;
    }
    .stSlider > div > div > div > div {
        color: #000000 !important;
    }
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
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("**Framework**")
    with col2:
        mode = st.radio("", ["RICE", "ICE"], horizontal=True)

    data = []
    for i, idea in enumerate(ideas):
        with st.expander(f"**{idea}**", expanded=i == 0):
            c1, c2 = st.columns(2)
            reach = c1.slider("Reach (users)", 0, 1000, 100, key=f"r{i}")
            impact = c1.slider("Impact (0–3)", 0, 3, 1, key=f"i{i}")
            confidence = c2.slider("Confidence %", 0, 100, 80, key=f"c{i}")
            effort = c2.slider("Effort (days)", 1, 30, 5, key=f"e{i}")

            score = (reach * impact * confidence / 100) / effort if mode == "RICE" else \
                    (impact * confidence * (100 - effort/30*100)) / 10000
            data.append({"Idea": idea, "Score": round(score, 1)})

    df = pd.DataFrame(data).sort_values("Score", ascending=False)

    st.success(f"**Top Idea:** {df.iloc[0]['Idea']} — {mode} Score: {df.iloc[0]['Score']}")

    fig = px.bar(
        df, x="Idea", y="Score", color="Score",
        color_continuous_scale="Blues",
        labels={"Score": f"{mode} Score"}
    ).update_layout(showlegend=False, height=360)
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Rankings", df.to_csv(index=False), f"{mode.lower()}_rankings.csv")
