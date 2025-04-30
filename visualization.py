import plotly.graph_objs as go

def plot_cumulative_probability(data):
    turns, probs = zip(*data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=turns, y=probs, mode='lines+markers', name='Cumulative Probability'))
    fig.update_layout(title="Cumulative Probability", xaxis_title="Turn", yaxis_title="Probability", yaxis_range=[0,1])
    return fig

def plot_turn_probability(data):
    turns, cumulative = zip(*data)
    turn_probs = [cumulative[0]] + [round(cumulative[i] - cumulative[i-1], 5) for i in range(1, len(cumulative))]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=turns, y=turn_probs, name='Turn Probability'))
    fig.update_layout(title="Probability of Ending on Turn", xaxis_title="Turn", yaxis_title="Probability", yaxis_range=[0, max(turn_probs) * 1.2])
    return fig
