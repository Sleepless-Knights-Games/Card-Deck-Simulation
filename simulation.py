import numpy as np

def simulate_game(
    initial_events: int,
    initial_blanks: int,
    max_turns: int,
    consecutive_events_to_end: int,
    simulations: int = 50000
):
    """
    Simulate your deck‐draw game `simulations` times, and return a list of
    (turn, cumulative_probability) from turn=1 to turn=max_turns.
    """

    # results[t] = number of games that ended exactly on turn t
    # index 0 unused; we'll use 1..max_turns
    results = np.zeros(max_turns + 1, dtype=int)

    for _ in range(simulations):
        deck = ['E'] * initial_events + ['B'] * initial_blanks
        revealed = []
        consecutive = 0
        ended = False

        for turn in range(1, max_turns + 1):
            # Draw a random card and remove it from the deck
            idx = np.random.randint(len(deck))
            card = deck.pop(idx)

            if card == 'E':
                revealed.append('E')
                consecutive += 1
                if consecutive >= consecutive_events_to_end:
                    results[turn] += 1
                    ended = True
                    break
            else:
                # Blank card: reset the streak, put revealed 'E's back, clear revealed
                consecutive = 0
                deck.extend(revealed)
                revealed = []

        # If we never hit the streak by max_turns, force it to count at max_turns
        if not ended:
            results[max_turns] += 1

    # Build cumulative distribution, dividing by the total number of simulations
    cum = np.cumsum(results) / simulations
    return list(zip(range(1, max_turns + 1), cum))
