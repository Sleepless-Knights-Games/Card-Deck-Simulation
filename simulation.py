import numpy as np

def simulate_game(initial_events, initial_blanks, max_turns, consecutive_events_to_end, simulations=10000):
    results = np.zeros(max_turns)
    
    for _ in range(simulations):
        deck = ['E'] * initial_events + ['B'] * initial_blanks
        revealed = []
        turn = 0
        consecutive = 0

        for t in range(max_turns):
            if not deck:
                break

            turn += 1
            drawn = np.random.choice(deck)
            deck.remove(drawn)

            if drawn == 'E':
                revealed.append('E')
                consecutive += 1
                if consecutive >= consecutive_events_to_end:
                    results[turn - 1] += 1
                    break
            else:
                deck += revealed
                revealed = []
                consecutive = 0

    cumulative = np.cumsum(results) / simulations
    return list(zip(range(1, max_turns + 1), cumulative))
