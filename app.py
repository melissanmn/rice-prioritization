import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RICE Prioritization", layout="wide")

# POPPINS FONT + LIGHT CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }
    .stApp { background: #f8fafc !important; }
    .main > div { background: #f8fafc !important; }
    .card {
        background: white !important;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    .stButton > button {
        background: #6366f1 !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
    }
    h1 { color: #6366f1 !important; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }
    .subtitle { text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 2rem; font-weight: 400; }
</style>
""", unsafe_allow_html=True)

# STATE
if "initiatives" not in st.session_state:
    st.session_state.initiatives = []

def rice_score(r, i, c, e):
    return round((r * i * (c / 100)) / e, 1) if e > 0 else 0

# HEADER
st.markdown("<h1>RICE Prioritization</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Clarify what to build next — simple, visual, fast.</p>", unsafe_allow_html=True)

# ADD BUTTON
if st.button("➕ Add Initiative", type="primary", use_container_width=True):
    st.session_state.show_form = True

# FORM
if st.session_state.get("show_form"):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### New Initiative")
        
        name = st.text_input("**Name**", placeholder="e.g. Fix login bug")
        
        col1, col2 = st.columns(2)
        with col1:
            reach = st.slider("**Reach** (users/month)", 0, 20000, 1000, 100)
        with col2:
            effort = st.slider("**Effort** (person-days)", 1, 30, 5, 1)
        
        col1, col2 = st.columns(2)
        with col1:
            impact = st.selectbox("**Impact**", [3,2,1,0.5,0.25], format_func=lambda x: {3:"High (3x)",2:"Medium (2x)",1:"Low (1x)",0.5:"Minimal",0.25:"Tiny"}[x])
        with col2:
            confidence = st.selectbox("**Confidence**", [100,90,80,70,60,50,40,30,20,10,0], format_func=lambda x: f"{x}%")

        score = rice_score(reach, impact, confidence, effort)
        st.metric("**Live RICE Score**", f"{score:.1f}", delta=None)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Add to List", type="primary", use_container_width=True):
                if name.strip():
                    st.session_state.initiatives.append({
                        "name": name, "reach": reach, "impact": impact,
                        "confidence": confidence, "effort": effort, "score": score
                    })
                    st.success(f"✅ **{name}** added! Score: {score:.1f}")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Name required")
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_form = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# RESULTS
if st.session_state.initiatives:
    df = pd.DataFrame(st.session_state.initiatives).sort_values("score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("**Top Priority**", df.iloc[0]["name"], df.iloc[0]["score"])
    with col2: st.metric("**Total**", len(df))
    with col3: st.metric("**Avg Score**", f"{df['score'].mean():.1f}")

    st.markdown('<div class="card"><h3>Priority Matrix</h3>', unsafe_allow_html=True)
    fig = px.scatter(df, x="effort", y="score", size="score", color="score", hover_name="name",
                     labels={"score":"RICE Score ↑","effort":"Effort (days) →"}, color_continuous_scale="Blues")
    fig.update_layout(height=500, title="Low Effort + High Score = DO FIRST", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>Ranked List</h3>', unsafe_allow_html=True)
    for _, row in df.iterrows():
        rank_color = "#10b981" if row["rank"] <= 3 else "#6b7280"
        st.markdown(f"""
        <div style="padding: 1rem; border-left: 4px solid {rank_color}; background: #f9fafb; border-radius: 8px; margin: 0.5rem 0">
            <div style="display: flex; justify-content: space-between; align-items: center">
                <span style="background: {rank_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600">#{row['rank']}</span>
                <strong style="font-size: 1.1rem; font-weight: 500">{row['name']}</strong>
                <span style="font-size: 1.5rem; font-weight: 700; color: #6366f1">{row['score']}</span>
            </div>
            <p style="margin: 0.5rem 0 0 0; color: #6b7280; font-weight: 400">
                👥 {row['reach']:,} users • ⏰ {row['effort']} days • 🎯 {row['impact']}x • 📊 {row['confidence']}%
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    csv = df.to_csv(index=False)
    st.download_button("📥 Export CSV", csv, "rice-priorities.csv", "text/csv")
else:
    st.info("Click **Add Initiative** to start.")
