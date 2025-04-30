import numpy as np

def simulate_game(initial_events, initial_blanks, max_turns, consecutive_events_to_end, num_simulations=50000):
    results = [0] * (max_turns + 1)

    for _ in range(num_simulations):
        revealed = []
        deck = ['E'] * initial_events + ['B'] * initial_blanks
        np.random.shuffle(deck)

        consecutive_events = 0
        turn = 1

        while turn <= max_turns and deck:
            card = deck.pop(0)  # Draw from the top

            if card == 'E':
                revealed.append(card)
                consecutive_events += 1
                if consecutive_events >= consecutive_events_to_end:
                    results[turn] += 1
                    break
            else:
                # Blank drawn
                consecutive_events = 0
                # Remove the blank (already done), reshuffle events back in
                deck.extend(revealed)
                revealed = []
                np.random.shuffle(deck)  # Shuffle after reshuffling in

            turn += 1

    total = sum(results)
    cumulative = 0
    prob_by_turn = []
    for i in range(1, max_turns + 1):
        cumulative += results[i]
        prob_by_turn.append((i, cumulative / total if total else 0))

    return prob_by_turn
