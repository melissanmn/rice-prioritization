import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Prioritize", layout="centered")

# INTER + SPACING (SAFE)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    .stApp {background: #FFFFFF; padding: 1rem;}
    .stTextArea > div > div > textarea {border-radius: 12px; border: 1px solid #D1D5DB; padding: 12px;}
    .stExpander {border-radius: 12px; border: 1px solid #E5E7EB; margin: 16px 0; background: #FAFBFC;}
    .stExpander > div > div {padding: 20px !important;}
    .stRadio {margin: 24px 0;}
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
            
            # NO HTML IN COLUMNS — USE st.empty() + spacing
            with c1:
                st.write("")  # spacer
                reach = st.slider("Reach (users)", 0, 1000, st.session_state[f"r{i}"])
                impact = st.slider("Impact (0–3)", 0, 3, st.session_state[f"i{i}"])
            with c2:
                st.write("")  # spacer
                confidence = st.slider("Confidence %", 0, 100, st.session_state[f"c{i}"])
                effort = st.slider("Effort (days)", 1, 30, st.session_state[f"e{i}"])

            # Save
            for val, param in zip([reach, impact, confidence, effort], ["r", "i", "c", "e"]):
                st.session_state[f"{param}{i}"] = val

            score = (reach * impact * confidence / 100) / effort if mode == "RICE" else \
                    (impact * confidence * (100 - effort/30*100)) / 10000
            data.append({"Idea": idea, "Score": round(score, 1)})

    df = pd.DataFrame(data).sort_values("Score", ascending=False)

    st.success(f"**Top Idea:** {df.iloc[0]['Idea']} — {mode} Score: {df.iloc[0]['Score']}")

    fig = px.bar(df, x="Idea", y="Score", color="Score", color_continuous_scale="Blues")
    fig.update_layout(showlegend=False, height=380, margin=dict(t=40))
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Rankings", df.to_csv(index=False), f"{mode.lower()}_rankings.csv")
