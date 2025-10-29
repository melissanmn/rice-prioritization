import streamlit as st
import pandas as pd
import plotly.express as px

# PURE WHITE, MINIMAL, FLAWLESS
st.set_page_config(page_title="Prioritize", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    .stApp {background: #FFFFFF;}
    .main {max-width: 720px; margin: auto; padding: 2rem 1rem;}
    .title {font-size: 40px; font-weight: 700; color: #111; text-align: center; margin: 0 0 8px;}
    .subtitle {font-size: 18px; color: #555; text-align: center; margin: 0 0 32px;}
    .stTextArea textarea {border-radius: 12px; border: 1px solid #E5E7EB; padding: 14px; font-size: 15px;}
    .stExpander {border: 1px solid #E5E7EB; border-radius: 12px; margin: 16px 0; background: #FFFFFF;}
    .stExpander > div > div {padding: 18px;}
    .stRadio > div {gap: 32px; justify-content: center; margin: 24px 0;}
    .stSlider > div > div > div {background: #F1F3F5;}
    .top-card {background: #F9FAFB; padding: 20px; border-radius: 12px; text-align: center; margin: 24px 0; border: 1px solid #E5E7EB;}
    .top-text {font-size: 19px; font-weight: 600; color: #111; margin: 0;}
    .top-score {font-size: 16px; color: #555; margin: 6px 0 0;}
</style>
""", unsafe_allow_html=True)

# CENTERED
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # HEADER
    st.markdown('<h1 class="title">Prioritize</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Rank your product ideas in seconds</p>', unsafe_allow_html=True)

    # INPUT
    ideas = st.text_area(
        "",
        "Add dark mode\nFix login bug\nBuild AI summary",
        height=120,
        placeholder="Type or paste ideas..."
    ).split("\n")
    ideas = [i.strip() for i in ideas if i.strip()]

    if ideas:
        mode = st.radio("Framework", ["RICE", "ICE"], horizontal=True)
        data = []

        for i, idea in enumerate(ideas):
            with st.expander(f"**{idea}**", expanded=True):
                c1, c2 = st.columns(2)
                reach = c1.slider("Reach", 0, 1000, 100, key=f"r{i}")
                impact = c1.slider("Impact", 0, 3, 1, key=f"i{i}")
                confidence = c2.slider("Confidence %", 0, 100, 80, key=f"c{i}")
                effort = c2.slider("Effort (days)", 1, 30, 5, key=f"e{i}")

                score = (reach * impact * confidence / 100) / effort if mode == "RICE" else \
                        (impact * confidence * (100 - effort/30*100)) / 10000
                data.append({"Idea": idea, "Score": round(score, 1), "Effort": effort})

        df = pd.DataFrame(data).sort_values("Score", ascending=False)

        # TOP IDEA CARD
        st.markdown(f'''
        <div class="top-card">
            <div class="top-text">Top Idea: <strong>{df.iloc[0]["Idea"]}</strong></div>
            <p class="top-score">{mode} Score: <strong>{df.iloc[0]["Score"]}</strong></p>
        </div>
        ''', unsafe_allow_html=True)

        # CHART
        fig = px.bar(
            df, x="Idea", y="Score", color="Effort",
            color_continuous_scale="Blues",
            labels={"Score": f"{mode} Score"}
        ).update_layout(
            showlegend=False, height=380,
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=14),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # EXPORT
        st.download_button("Export CSV", df.to_csv(index=False), f"{mode.lower()}_rankings.csv", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
