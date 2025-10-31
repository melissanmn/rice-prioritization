import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RICE Prioritization", layout="wide")

# LIGHT THEME + CLEAN CSS
st.markdown("""
<style>
    .main {background: #f8fafc; padding: 2rem}
    .stMetric {background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin: 0.5rem 0}
    .card {background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 1rem 0}
    .stButton > button {background: #6366f1; color: white; border-radius: 12px; font-weight: 600}
    h1 {color: #6366f1; font-weight: 800; text-align: center}
    .stTextInput > div > div > input {border-radius: 8px; padding: 0.5rem}
</style>
""", unsafe_allow_html=True)

# STATE
if "initiatives" not in st.session_state:
    st.session_state.initiatives = []

def rice_score(r, i, c, e):
    return round((r * i * (c / 100)) / e, 1) if e > 0 else 0

# HEADER
st.markdown("<h1>RICE Prioritization</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b'>Clarify what to build next — simple, visual, fast.</p>", unsafe_allow_html=True)

# ADD BUTTON
if st.button("➕ Add Initiative", type="primary", use_container_width=True):
    st.session_state.show_form = True

# FORM
if st.session_state.get("show_form"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### New Initiative")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("**Name**", placeholder="e.g. Fix login bug")
        reach = st.number_input("**Reach** (users/month)", 0, 100000, 1000, 100)
    with c2:
        effort = st.number_input("**Effort** (person-days)", 1, 30, 5)
        impact = st.selectbox("**Impact**", [3,2,1,0.5,0.25], format_func=lambda x: {3:"High (3x)",2:"Medium (2x)",1:"Low (1x)",0.5:"Minimal",0.25:"Tiny"}[x])
    confidence = st.slider("**Confidence (%)**", 0, 100, 80)
    score = rice_score(reach, impact, confidence, effort)
    st.metric("**Live Score**", score)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Add", type="primary"):
            if name.strip():
                st.session_state.initiatives.append({"name":name,"reach":reach,"impact":impact,"confidence":confidence,"effort":effort,"score":score})
                st.success("Added!")
                st.session_state.show_form = False
                st.rerun()
    with c2:
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# RESULTS
if st.session_state.initiatives:
    df = pd.DataFrame(st.session_state.initiatives).sort_values("score", ascending=False).reset_index(drop=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Top Priority", df.iloc[0].name, df.iloc[0].score)
    with c2: st.metric("Total", len(df))
    with c3: st.metric("Avg Score", f"{df.score.mean():.1f}")

    st.markdown('<div class="card"><h3>Priority Matrix</h3>', unsafe_allow_html=True)
    fig = px.scatter(df, x="effort", y="score", size="score", color="score", hover_name="name", color_continuous_scale="Blues")
    fig.update_layout(height=500, title="Low Effort + High Score = DO FIRST", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>Ranked List</h3>', unsafe_allow_html=True)
    for i, r in df.iterrows():
        st.markdown(f"**#{i+1} {r.name}** — **{r.score}** | {r.reach:,} users | {r.effort}d | {r.impact}x | {r.confidence}%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button("Export CSV", df.to_csv(index=False), "rice.csv")

else:
    st.info("Click **Add Initiative** to start prioritizing.")
