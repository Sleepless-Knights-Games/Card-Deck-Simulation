import numpy as np

def simulate_game_corrected(initial_events, initial_blanks, max_turns, consecutive_events_to_end, num_simulations=50000):
    results = [0] * (max_turns + 1)

    for _ in range(num_simulations):
        # Initialise the deck
        deck = ['E'] * initial_events + ['B'] * initial_blanks
        np.random.shuffle(deck)
        revealed = []

        consecutive_events = 0
        turn = 1

        while turn <= max_turns and deck:
            card = deck.pop(0)

            if card == 'E':
                revealed.append('E')
                consecutive_events += 1
                if consecutive_events >= consecutive_events_to_end:
                    results[turn] += 1
                    break
            else:
                # Blank resets consecutive counter
                consecutive_events = 0
                # Return revealed events to the deck and reshuffle
                deck.extend(revealed)
                np.random.shuffle(deck)
                revealed = []

            turn += 1

        # If we reached the end without triggering, record nothing (will count in total)

    total = sum(results)
    cumulative = 0
    prob_by_turn = []
    for i in range(1, max_turns + 1):
        cumulative += results[i]
        prob = cumulative / total if total else 0
        prob_by_turn.append((i, prob))

    return prob_by_turn
