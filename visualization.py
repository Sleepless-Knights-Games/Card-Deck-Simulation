import plotly.graph_objs as go

def plot_cumulative_probability(data):
    turns, cum_probs = zip(*data)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=turns, y=cum_probs, mode="lines+markers", name="Cumulative")
    )
    fig.update_layout(
        xaxis_title="Turn",
        yaxis_title="Cumulative Probability",
        yaxis_range=[0, 1],
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def plot_turn_probability(data):
    turns, cum_probs = zip(*data)
    turn_probs = [cum_probs[0]] + [
        cum_probs[i] - cum_probs[i - 1] for i in range(1, len(cum_probs))
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=turns, y=turn_probs, name="Per Turn")
    )
    fig.update_layout(
        xaxis_title="Turn",
        yaxis_title="Probability",
        yaxis_range=[0, max(turn_probs) * 1.1],
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig
