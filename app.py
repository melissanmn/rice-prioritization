import streamlit as st
import pandas as pd
import plotly.express as px

st.title("RICE Prioritization Calculator")
st.caption("Paste your ideas. Rank them. Ship the best.")

ideas = st.text_area("Enter ideas (one per line)", "Add dark mode\nFix login bug\nBuild AI summary").split("\n")
ideas = [i.strip() for i in ideas if i.strip()]

if ideas:
    data = []
    for i, idea in enumerate(ideas):
        col1, col2, col3, col4 = st.columns(4)
        reach = col1.slider(f"Reach (users in 3mo)", 0, 1000, 100, key=f"r{i}")
        impact = col2.slider(f"Impact (0–3)", 0, 3, 1, key=f"i{i}")
        confidence = col3.slider(f"Confidence %", 0, 100, 80, key=f"c{i}")
        effort = col4.slider(f"Effort (person-days)", 1, 30, 5, key=f"e{i}")
        
        rice = (reach * impact * confidence / 100) / effort
        data.append({"Idea": idea, "RICE": round(rice, 1), "Effort": effort})
    
    df = pd.DataFrame(data).sort_values("RICE", ascending=False)
    st.success("### Ranked Ideas")
    st.dataframe(df.style.highlight_max(axis=0, subset=["RICE"]), use_container_width=True)
    
    # Chart
    fig = px.bar(df, x="Idea", y="RICE", color="Effort", title="RICE Score vs Effort")
    st.plotly_chart(fig, use_container_width=True)
    
    # Export
    csv = df.to_csv(index=False)
    st.download_button("Download Rankings", csv, "rice_rankings.csv")
