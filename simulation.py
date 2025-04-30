import random

def simulate_game(deck, num_turns):
    draws = []
    for _ in range(num_turns):
        draw = random.choice(deck)
        draws.append(draw)

    cumulative_count = {}
    for i, card in enumerate(draws, 1):
        cumulative_count[card] = cumulative_count.get(card, 0) + 1

    return {
        "draws": draws,
        "cumulative_count": cumulative_count
    }
