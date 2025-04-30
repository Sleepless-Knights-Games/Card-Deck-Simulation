import plotly.graph_objs as go

def plot_cumulative_probability(prob_results):
    turns, probs = zip(*prob_results)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=turns, y=probs, mode='lines', name='Cumulative'))
    fig.update_layout(xaxis_title='Turn', yaxis_title='Cumulative Probability')
    return fig

def plot_turn_probability(prob_results):
    turns, probs = zip(*prob_results)
    diffs = [probs[0]] + [probs[i] - probs[i - 1] for i in range(1, len(probs))]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=turns, y=diffs, name='Per Turn'))
    fig.update_layout(xaxis_title='Turn', yaxis_title='Probability')
    return fig
