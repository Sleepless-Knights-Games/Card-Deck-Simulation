import streamlit as st
import pandas as pd
import numpy as np
from simulation import simulate_game
from visualization import plot_cumulative_probability, plot_turn_probability

st.set_page_config(page_title="Card Game Probability Simulator", page_icon="🃏", layout="wide")

st.title("Card Game Probability Simulator")
st.markdown("""
This tool simulates the probability of a card game ending by a specific turn.
Adjust the parameters below to see how they affect the outcome.
""")

st.sidebar.header("Game Parameters")

initial_events = st.sidebar.slider("Initial Events", 1, 20, 5)
initial_blanks = st.sidebar.slider("Initial Blanks", 1, 50, 15)
max_turns = st.sidebar.slider("Maximum Turns to Simulate", 10, 100, 48)

with st.sidebar.expander("Advanced Settings"):
    consecutive_events_to_end = st.number_input("Consecutive Events to End Round", 1, 10, 3)
    show_detailed_data = st.checkbox("Show Detailed Data Table", value=False)

if st.sidebar.button("Run Simulation") or 'prob_results' not in st.session_state:
    with st.spinner("Running simulation..."):
        prob_results = simulate_game(initial_events, initial_blanks, max_turns, consecutive_events_to_end)
        st.session_state.prob_results = prob_results
        st.session_state.params = {
            'initial_events': initial_events,
            'initial_blanks': initial_blanks,
            'max_turns': max_turns,
            'consecutive_events_to_end': consecutive_events_to_end
        }
else:
    prob_results = st.session_state.prob_results

st.subheader("Current Simulation Parameters")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Initial Events", st.session_state.params['initial_events'])
col2.metric("Initial Blanks", st.session_state.params['initial_blanks'])
col3.metric("Max Turns", st.session_state.params['max_turns'])
col4.metric("Events to End Round", st.session_state.params['consecutive_events_to_end'])

total_cards = initial_events + initial_blanks
st.info(f"Total deck size: {total_cards} cards")
st.info(f"Ratio of Events to Blanks: 1:{initial_blanks / initial_events:.2f}")

st.subheader("Probability Visualization")
col1, col2 = st.columns(2)

with col1:
    st.write("Cumulative Probability of Game Ending by Turn")
    st.plotly_chart(plot_cumulative_probability(prob_results), use_container_width=True)

with col2:
    st.write("Probability of Game Ending on Specific Turn")
    st.plotly_chart(plot_turn_probability(prob_results), use_container_width=True)

st.subheader("Key Statistics")

df = pd.DataFrame(prob_results, columns=["Turn", "Cumulative Probability"])
df["Turn Probability"] = df["Cumulative Probability"].diff().fillna(df["Cumulative Probability"].iloc[0])
median_turn = df[df["Cumulative Probability"] >= 0.5].iloc[0]["Turn"] if any(df["Cumulative Probability"] >= 0.5) else "N/A"
most_likely_turn = df.iloc[df["Turn Probability"].argmax()]["Turn"]
confidence_90 = df[df["Cumulative Probability"] >= 0.9].iloc[0]["Turn"] if any(df["Cumulative Probability"] >= 0.9) else "N/A"
prob_10_turns = df[df["Turn"] <= 10].iloc[-1]["Cumulative Probability"] if len(df[df["Turn"] <= 10]) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Median Game Length", f"{median_turn} turns")
col2.metric("Most Likely End Turn", f"{most_likely_turn} turns")
col3.metric("90% of Games End By", f"{confidence_90} turns")
col4.metric("Ends in First 10 Turns", f"{prob_10_turns:.1%}")

if show_detailed_data:
    st.subheader("Detailed Probability Data")
    display_df = df.copy()
    display_df["Cumulative Probability"] = display_df["Cumulative Probability"].apply(lambda x: f"{x:.5f}")
    display_df["Turn Probability"] = display_df["Turn Probability"].apply(lambda x: f"{x:.5f}")
    st.dataframe(display_df)

st.subheader("Simulation Explanation")
st.markdown("""
### How the Simulation Works
1. The deck starts with a mix of event and blank cards.
2. On each turn, a card is drawn. Event cards go into play; blank cards discard events.
3. The game ends after a chosen number of **consecutive event cards** are drawn.

This simulation estimates the probability of the game ending on each turn.
""")
