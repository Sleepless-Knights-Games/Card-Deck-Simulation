import streamlit as st
import pandas as pd
from simulation import simulate_game
from visualization import plot_cumulative_probability, plot_turn_probability

st.set_page_config(page_title="Card Game Probability Simulator", page_icon="🃏", layout="wide")

st.title("Card Game Probability Simulator")
st.markdown("""
Simulates the probability of your card game ending by each turn, given a deck of event and blank cards.
""")

# Sidebar inputs
st.sidebar.header("Game Parameters")
initial_events = st.sidebar.slider("Initial Events", 1, 20, 5)
initial_blanks = st.sidebar.slider("Initial Blanks", 1, 50, 15)
max_turns = st.sidebar.slider("Maximum Turns to Simulate", 10, 100, 48)

with st.sidebar.expander("Advanced Settings"):
    consecutive_events_to_end = st.number_input("Consecutive Events to End Round", 1, 10, 3)
    show_detailed_data = st.checkbox("Show Detailed Data Table", value=False)

# Run simulation when button clicked or first load
if st.sidebar.button("Run Simulation") or "prob_results" not in st.session_state:
    with st.spinner("Running simulation..."):
        st.session_state.prob_results = simulate_game(
            initial_events=initial_events,
            initial_blanks=initial_blanks,
            max_turns=max_turns,
            consecutive_events_to_end=consecutive_events_to_end
        )
        st.session_state.params = {
            "initial_events": initial_events,
            "initial_blanks": initial_blanks,
            "max_turns": max_turns,
            "consecutive_events_to_end": consecutive_events_to_end
        }

# Retrieve results
prob_results = st.session_state.prob_results
params = st.session_state.params

# Display parameters
st.subheader("Current Simulation Parameters")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Events", params["initial_events"])
c2.metric("Blanks", params["initial_blanks"])
c3.metric("Max Turns", params["max_turns"])
c4.metric("Consec. to End", params["consecutive_events_to_end"])

# Deck info
total = params["initial_events"] + params["initial_blanks"]
st.info(f"Deck size: {total} cards (E:{params['initial_events']}, B:{params['initial_blanks']})")

# Charts
st.subheader("Probability Visualization")
col1, col2 = st.columns(2)

with col1:
    st.write("Cumulative Probability by Turn")
    st.plotly_chart(plot_cumulative_probability(prob_results), use_container_width=True)

with col2:
    st.write("Probability on Exact Turn")
    st.plotly_chart(plot_turn_probability(prob_results), use_container_width=True)

# Key stats
df = pd.DataFrame(prob_results, columns=["Turn", "Cumulative"])
df["Per Turn"] = df["Cumulative"].diff().fillna(df["Cumulative"].iloc[0])

median = df[df["Cumulative"] >= 0.5].iloc[0]["Turn"]
peak = df.iloc[df["Per Turn"].idxmax()]["Turn"]
p90 = df[df["Cumulative"] >= 0.9].iloc[0]["Turn"]
p10 = df[df["Turn"] <= 10].iloc[-1]["Cumulative"]

st.subheader("Key Statistics")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Median End Turn", f"{int(median)}")
s2.metric("Most Likely End Turn", f"{int(peak)}")
s3.metric("90% by Turn", f"{int(p90)}")
s4.metric("≤10 Turns", f"{p10:.1%}")

# Detailed table if requested
if show_detailed_data:
    st.subheader("Detailed Data")
    df_display = df.copy()
    df_display["Cumulative"] = df_display["Cumulative"].map("{:.5f}".format)
    df_display["Per Turn"] = df_display["Per Turn"].map("{:.5f}".format)
    st.dataframe(df_display, use_container_width=True)
