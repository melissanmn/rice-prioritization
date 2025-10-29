import streamlit as st
import pandas as pd
import plotly.express as px

# CLEAN, NATIVE, BEAUTIFUL
st.set_page_config(page_title="Prioritize", layout="centered", initial_sidebar_state="collapsed")

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
            effort = c2.slider("Effort (person-days)", 1, 30, 5, key=f"e{i}")

            score = (reach * impact * confidence / 100) / effort if mode == "RICE" else \
                    (impact * confidence * (100 - effort/30*100)) / 10000
            data.append({"Idea": idea, "Score": round(score, 1)})

    df = pd.DataFrame(data).sort_values("Score", ascending=False)

    # TOP IDEA
    st.success(f"**Top Idea:** {df.iloc[0]['Idea']} — {mode} Score: {df.iloc[0]['Score']}")

    # CHART
    fig = px.bar(
        df, x="Idea", y="Score", color="Score",
        color_continuous_scale="Blues",
        labels={"Score": f"{mode} Score"}
    ).update_layout(showlegend=False, height=360)
    st.plotly_chart(fig, use_container_width=True)

    # EXPORT
    st.download_button(
        "Download Rankings",
        df.to_csv(index=False),
        f"{mode.lower()}_rankings.csv",
        "text/csv"
    )
