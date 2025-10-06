import os, json
import streamlit as st
import pandas as pd
from agent.db import fetch_schema_catalog, run_sql
from agent.llm import nlsql, summarize_df
from agent.charting import render_chart

st.set_page_config(page_title="LLM Analytics Agent", layout="wide")
st.title("🧠 LLM Analytics Agent – Postgres + OpenAI + Streamlit")



st.markdown("Enter a **business question**. The agent will generate SQL, run it, chart results, and summarize insights.")
question = st.text_input("Business question", value="Show sales by product in the year 2024.")

colA, colB = st.columns([1,1])
with colA:
    if st.button("Generate SQL"):
        with st.spinner("Introspecting schema & drafting SQL..."):
            schema = fetch_schema_catalog()
            sql = nlsql(question, schema=schema, model='gpt-4o-mini-2024-07-18')
            st.session_state["sql"] = sql

with colB:
    run_clicked = st.button("Run Query")

sql = st.session_state.get("sql", "")

st.subheader("Proposed SQL")
st.code(sql or "(no SQL yet)", language="sql")

if run_clicked and sql:
    with st.spinner("Running query..."):
        try:
            df = run_sql(sql)
        except Exception as e:
            st.error(f"Query failed: {e}")
            df = None
    if df is not None and not df.empty:
        st.subheader("Results")
        st.dataframe(df, use_container_width=True)
        fig = render_chart(df)
        if fig:
            st.pyplot(fig, use_container_width=True)
        with st.spinner("Summarizing insights..."):
            insights = summarize_df(df, model='gpt-4o-mini-2024-07-18')
        st.subheader("Insights")
        st.markdown(insights)
    else:
        st.info("No rows returned.")
