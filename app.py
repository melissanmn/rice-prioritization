import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="RICE Prioritization", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Figma-style
st.markdown("""
<style>
    .main {padding: 2rem}
    .stMetric {background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05)}
    .card {background: white; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 1rem 0}
</style>
""", unsafe_allow_html=True)

if "initiatives" not in st.session_state:
    st.session_state.initiatives = []

def rice_score(r, i, c, e):
    return (r * i * (c / 100)) / e if e > 0 else 0

# HEADER
st.markdown("""
<div style='text-align:center; padding: 2rem'>
    <h1 style='color: #6366f1; font-size: 3rem; margin:0; font-weight: 800'>
        RICE Prioritization
    </h1>
    <p style='color: #64748b; font-size: 1.2rem; margin: 0.5rem 0 2rem'>
        Clarify what to build next
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    st.markdown("### ✨ Add your first initiative")
with col2:
    if st.button("➕ **Add Initiative**", use_container_width=True):
        st.session_state.show_form = True

# FORM
if st.session_state.get("show_form", False):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### **New Initiative**")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("**Name**", placeholder="Fix login bug")
            reach = st.number_input("**Reach** (users/month)", min_value=0, value=1000, step=100)
        with col2:
            effort = st.number_input("**Effort** (person-days)", min_value=1, value=5)
            impact = st.selectbox("**Impact**", [3,2,1,0.5,0.25], 
                                format_func=lambda x: f"{x}x {'⭐⭐⭐' if x==3 else '⭐⭐' if x==2 else '⭐'}"})
        
        confidence = st.slider("**Confidence** %", 0, 100, 80)
        
        col1, col2 = st.columns(2)
        score = rice_score(reach, impact, confidence, effort)
        col1.metric("**Live Score**", f"{score:.0f}", delta=None)
        
        with col2:
            if st.button("✅ **Add to Priority List**", type="primary", use_container_width=True):
                if name:
                    st.session_state.initiatives.append({
                        "name": name, "reach": reach, "impact": impact,
                        "confidence": confidence, "effort": effort, "score": round(score, 1)
                    })
                    st.success("✅ **Added!**")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("❌ **Name required**")
            if st.button("❌ **Cancel**", use_container_width=True):
                st.session_state.show_form = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# RESULTS
if st.session_state.initiatives:
    df = pd.DataFrame(st.session_state.initiatives)
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    
    # METRICS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🥇 **#1 Priority**", df.iloc[0]["name"][:30]+"...", f"{df.iloc[0].score:.0f}")
    with col2:
        st.metric("📊 **Total Ideas**", len(df))
    with col3:
        st.metric("🎯 **Avg Score**", f"{df.score.mean():.0f}")
    
    # PRIORITY MATRIX
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### **🎯 Priority Matrix**")
    fig = px.scatter(df, x="effort", y="score", size="score", 
                    hover_name="name", hover_data=["reach", "effort"],
                    title="**Low Effort + High Score = DO FIRST**",
                    labels={"score": "RICE Score", "effort": "Effort (days)"})
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # RANKED LIST
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### **📋 Ranked Priority List**")
    
    for i, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([1,4,1])
            with col1:
                st.markdown(f"**#{i+1}**")
            with col2:
                st.markdown(f"### **{row['name']}**")
                st.caption(f"👥 {row['reach']:,} users | ⏰ {row['effort']}d | 🎯 {row['impact']}x | 📊 {row['confidence']}%")
            with col2:
                st.metric("Score", row['score'], delta=None)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # EXPORT
    csv = df.to_csv(index=False)
    st.download_button("📥 **Export CSV**", csv, "rice-priorities.csv")

else:
    st.markdown('<div class="card" style="text-align:center">', unsafe_allow_html=True)
    st.markdown("""
    <h3>🚀 **Ready to prioritize?**</h3>
    <p>Add your first initiative above to see the magic ✨</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

