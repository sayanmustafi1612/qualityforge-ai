"""
Streamlit dashboard: automation health at a glance.

Run with: streamlit run dashboard/app.py
Reads from the same SQLite history DB that conftest.py writes to, so it
reflects every local or CI run without any extra wiring.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from utils.failure_analyzer import compute_health
from utils.results_store import fetch_history

st.set_page_config(page_title="QualityForge AI — Quality Dashboard", layout="wide")
st.title("🧪 QualityForge AI — Quality Dashboard")

history = fetch_history()
if not history:
    st.info("No test runs recorded yet. Run `pytest` at least a few times to populate this dashboard.")
    st.stop()

health = [t.as_dict() for t in compute_health(min_runs=1)]
df = pd.DataFrame(health)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tests tracked", len(df))
col2.metric("🔴 Broken", int((df["status"] == "BROKEN").sum()))
col3.metric("🟡 Flaky / High flakiness", int(df["status"].isin(["FLAKY", "HIGH_FLAKINESS"]).sum()))
col4.metric("🟢 Stable", int((df["status"] == "STABLE").sum()))

st.subheader("Test health")
st.dataframe(
    df.sort_values("flakiness_score", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Average duration by test (ms)")
st.bar_chart(df.set_index("test_name")["avg_duration_ms"])

st.subheader("Raw execution history (most recent first)")
raw_df = pd.DataFrame(history)
st.dataframe(raw_df.head(200), use_container_width=True, hide_index=True)
