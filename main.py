import streamlit as st
import pandas as pd
from simulation import simulate_game
from visualization import plot_cumulative_probability, plot_turn_probability

st.set_page_config(page_title="Card Game Probability Simulator", page_icon="🎴")

st.title("Card Game Probability Simulator")

deck_input = st.text_input("Enter your deck (comma-separated cards):", "A,B,C,D,E")
deck = deck_input.split(',')

turns = st.slider("Number of Turns to Simulate", 1, 100, 10)

if st.button("Run Simulation"):
    sim_result = simulate_game(deck, turns)
    
    st.subheader("Simulation Draws")
    st.write(sim_result["draws"])
    
    st.subheader("Cumulative Counts")
    st.write(sim_result["cumulative_count"])

    st.subheader("Cumulative Probability Plot")
    st.pyplot(plot_cumulative_probability(sim_result))

    st.subheader("Turn Probability Plot")
    st.pyplot(plot_turn_probability(sim_result))
