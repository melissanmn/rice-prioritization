import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RICE Prioritization", layout="wide")

# LOAD MODERN FONT
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stApp { background: #f8fafc; }
    .card { background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 1rem 0; }
    .stButton > button { background: #6366f1; color: white; border-radius: 12px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

if "initiatives" not in st.session_state:
    st.session_state.initiatives = []

def rice_score(r, i, c, e):
    return round((r * i * (c / 100)) / e, 1) if e > 0 else 0

st.markdown("<h1 style='text-align:center; color:#6366f1'>RICE Prioritization</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b'>Clarify what to build next — simple, visual, fast.</p>", unsafe_allow_html=True)

if st.button("➕ Add Initiative", type="primary"):
    st.session_state.show_form = True

if st.session_state.get("show_form"):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("Name", "Fix login bug")
        c1, c2 = st.columns(2)
        with c1: reach = st.slider("Reach (users/mo)", 0, 20000, 1000, 100)
        with c2: effort = st.slider("Effort (days)", 1, 30, 5)
        c1, c2 = st.columns(2)
        with c1: impact = st.selectbox("Impact", [3,2,1,0.5,0.25], format_func=lambda x: f"{x}x")
        with c2: confidence = st.selectbox("Confidence", range(0,101,10), format_func=lambda x: f"{x}%")
        score = rice_score(reach, impact, confidence, effort)
        st.metric("Live Score", score)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Add", type="primary"):
                if name: 
                    st.session_state.initiatives.append({"name":name, "reach":reach, "impact":impact, "confidence":confidence, "effort":effort, "score":score})
                    st.success("Added!")
                    st.session_state.show_form = False
                    st.rerun()
        with c2:
            if st.button("Cancel"): 
                st.session_state.show_form = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.initiatives:
    df = pd.DataFrame(st.session_state.initiatives).sort_values("score", ascending=False)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Top", df.iloc[0].name, df.iloc[0].score)
    with c2: st.metric("Total", len(df))
    with c3: st.metric("Avg", f"{df.score.mean():.1f}")

    st.markdown('<div class="card"><h3>Matrix</h3>', unsafe_allow_html=True)
    fig = px.scatter(df, x="effort", y="score", size="score", color="score", hover_name="name", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button("Export CSV", df.to_csv(index=False), "rice.csv")
else:
    st.info("Click Add Initiative to start.")
