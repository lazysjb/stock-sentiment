import matplotlib.pyplot as plt


def plot_time_series(df,
                     figsize=(8, 6),
                     title=None):
    """Assume input dataframe (df) has index as dates"""
    fig, ax = plt.subplots(figsize=figsize)
    df.plot(ax=ax)

    if title is not None:
        ax.set_title(title)
