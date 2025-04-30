import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_cumulative_probability(sim_result):
    data = sim_result["draws"]
    df = pd.DataFrame({"Draws": data})
    plot = sns.histplot(data=df, x="Draws", stat="probability", kde=False)
    fig = plot.get_figure()
    fig.tight_layout()
    return fig

def plot_turn_probability(sim_result):
    data = sim_result["draws"]
    df = pd.DataFrame({"Turn": range(1, len(data)+1), "Draw": data})
    fig, ax = plt.subplots()
    sns.countplot(x="Draw", data=df, ax=ax)
    ax.set_title("Draw Frequency by Card")
    return fig
