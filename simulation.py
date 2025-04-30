import numpy as np

def simulate_game(initial_events, initial_blanks, max_turns, consecutive_events_to_end, simulations=50000):
    """
    Simulate the card‐draw game and return a list of (turn, cumulative_probability).
    Rules:
      - Deck starts with initial_events 'E' cards and initial_blanks 'B' cards.
      - Each turn: draw one random card from deck.
        * If 'E': put it in revealed pile; if you hit consecutive_events_to_end in a row, record end on that turn.
        * If 'B': reset consecutive count, remove that blank, shuffle all revealed 'E's back into deck, clear revealed.
      - Stop either when you hit the end condition or when max_turns is reached.
    """
    # results[t] = count of games that ended exactly on turn t
    results = np.zeros(max_turns + 1, dtype=int)

    for _ in range(simulations):
        # 1) Initialize deck & state
        deck = ['E'] * initial_events + ['B'] * initial_blanks
        revealed = []
        consecutive = 0

        # 2) Play turns
        for turn in range(1, max_turns + 1):
            if not deck:
                break
            # draw random card
            idx = np.random.randint(len(deck))
            card = deck.pop(idx)

            if card == 'E':
                revealed.append('E')
                consecutive += 1
                if consecutive >= consecutive_events_to_end:
                    results[turn] += 1
                    break
            else:  # blank drawn
                consecutive = 0
                # put revealed events back into deck and reshuffle
                deck.extend(revealed)
                np.random.shuffle(deck)
                revealed = []

    # 3) Build cumulative probability list
    total_ended = results.sum()
    cumulative = 0
    output = []
    for turn in range(1, max_turns + 1):
        cumulative += results[turn]
        prob = cumulative / total_ended if total_ended > 0 else 0.0
        output.append((turn, prob))

    return output
