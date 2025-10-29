import streamlit as st
import pandas as pd
import plotly.express as px

st.title("RICE / ICE Prioritization Calculator")
st.caption("Enter ideas. Adjust sliders. Get ranked results instantly.")

ideas = st.text_area("Enter ideas (one per line)", "Add dark mode\nFix login bug\nBuild AI summary").split("\n")
ideas = [i.strip() for i in ideas if i.strip()]

if ideas:
    data = []
    mode = st.radio("Scoring", ["RICE", "ICE"], horizontal=True)

    for i, idea in enumerate(ideas):
        col1, col2, col3, col4 = st.columns(4)
        reach = col1.slider(f"Reach (users in 3mo)", 0, 1000, 100, key=f"r{i}")
        impact = col2.slider(f"Impact (0–3)", 0, 3, 1, key=f"i{i}")
        confidence = col3.slider(f"Confidence %", 0, 100, 80, key=f"c{i}")
        effort = col4.slider(f"Effort (person-days)", 1, 30, 5, key=f"e{i}")
        
        if mode == "RICE":
            score = (reach * impact * confidence / 100) / effort
        else:  # ICE
            score = (impact * confidence * (100 - effort/30*100)) / 10000
        
        data.append({"Idea": idea, "Score": round(score, 1), "Effort": effort})
    
    df = pd.DataFrame(data).sort_values("Score", ascending=False)
    st.success(f"### Ranked Ideas ({mode})")
    st.dataframe(df.style.highlight_max(axis=0, subset=["Score"]), use_container_width=True)
    
    fig = px.bar(df, x="Idea", y="Score", color="Effort", title=f"{mode} Score vs Effort")
    st.plotly_chart(fig, use_container_width=True)
    
    csv = df.to_csv(index=False)
    st.download_button("Download Rankings", csv, f"{mode.lower()}_rankings.csv")
