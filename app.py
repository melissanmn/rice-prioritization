import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="RICE Prioritization", layout="wide")
sns.set_style("white")

if "initiatives" not in st.session_state:
    st.session_state.initiatives = []

def rice_score(r, i, c, e):
    return (r * i * (c / 100)) / e if e > 0 else 0

col1, col2 = st.columns([3, 1])
with col1:
    st.title("RICE Prioritization")
    st.caption("Clarify what to build next — simple, visual, fast.")
with col2:
    if st.button("Add Initiative", type="primary", use_container_width=True):
        st.session_state.show_form = True

if st.session_state.get("show_form"):
    with st.expander("**New Initiative**", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Initiative Name", placeholder="e.g. Fix login bug")
            reach = st.slider("Reach (users/month)", 0, 20000, 1000, 100)
        with c2:
            effort = st.slider("Effort (person-days)", 1, 30, 5)
            impact = st.selectbox("Impact", [3, 2, 1, 0.5, 0.25],
                format_func=lambda x: {3:"High (3x)", 2:"Medium (2x)", 1:"Low (1x)", 0.5:"Minimal (0.5x)", 0.25:"Tiny (0.25x)"}[x]
            )
        confidence = st.slider("Confidence (%)", 0, 100, 80, 5)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Add to List", type="primary", use_container_width=True):
                if name.strip():
                    score = rice_score(reach, impact, confidence, effort)
                    st.session_state.initiatives.append({
                        "name": name, "reach": reach, "impact": impact,
                        "confidence": confidence, "effort": effort, "score": round(score, 1)
                    })
                    st.success(f"**{name}** added → Score: **{score:.1f}**")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Name required")
        with c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_form = False
                st.rerun()

if st.session_state.initiatives:
    df = pd.DataFrame(st.session_state.initiatives)
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Top Priority", df.iloc[0]["name"], f"Score: {df.iloc[0]['score']}")
    with c2:
        st.metric("Total Initiatives", len(df))
    with c3:
        st.metric("Avg Score", f"{df['score'].mean():.1f}")

    st.markdown("---")
    st.subheader("Priority Matrix")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('#f9f9f9')
    median_score = df['score'].median()
    median_effort = df['effort'].median()
    ax.axhline(median_score, color='gray', alpha=0.5)
    ax.axvline(median_effort, color='gray', alpha=0.5)
    ax.text(median_effort/2, df['score'].max() * 0.9, "DO FIRST", ha='center', fontweight='bold', color='#1a5fb4')
    ax.scatter(df['effort'], df['score'], c=['#1a5fb4' if s > median_score else '#9ca3af' for s in df['score']], 
               s=[100 + (s - df['score'].min()) * 10 for s in df['score']], alpha=0.8, edgecolors='white', linewidth=2)
    for i in range(min(3, len(df))):
        row = df.iloc[i]
        ax.annotate(f"  #{i+1} {row['name'][:15]}", (row['effort'], row['score']), fontsize=9, fontweight='bold')
    ax.set_xlabel("Effort")
    ax.set_ylabel("RICE Score")
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Ranked Initiatives")
    for _, row in df.iterrows():
        st.markdown(f"""
        <div style="padding: 1rem; margin: 0.5rem 0; border-radius: 12px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background: #eef2ff; color: #5c7cfa; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">
                        #{row['rank']}
                    </span>
                    <strong style="margin-left: 8px; font-size: 1.1rem;">{row['name']}</strong>
                </div>
                <span style="background: {'bg-green-100 text-green-800' if row['rank'] <= 3 else 'bg-gray-100 text-gray-800'}; padding: 6px 12px; border-radius: 20px; font-weight: bold;">
                    {row['score']} pts
                </span>
            </div>
            <div style="margin-top: 8px; font-size: 0.9rem; color: #666;">
                Users: {row['reach']:,} · Effort: {row['effort']}d · Impact: {row['impact']}x · Confidence: {row['confidence']}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    csv = df.to_csv(index=False)
    st.download_button("Export as CSV", csv, "rice-priorities.csv", "text/csv")
else:
    st.info("Click **Add Initiative** to get started.")
