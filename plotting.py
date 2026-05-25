import matplotlib.pyplot as plt


def plot_yield_curve(country: str, curve_data: dict):

    maturities = curve_data["maturities"]

    current_curve = curve_data["current_curve"]
    previous_curve = curve_data["previous_curve"]

    latest_date = curve_data["latest_date"]
    previous_date = curve_data["previous_date"]

    # Smaller figure
    fig, ax = plt.subplots(figsize=(7, 4))

    # Current
    ax.plot(
        maturities,
        current_curve,
        marker="o",
        linewidth=2.5,
        label=f"Current ({latest_date.date()})"
    )

    # Previous
    ax.plot(
        maturities,
        previous_curve,
        linestyle="--",
        marker="x",
        linewidth=2,
        label=f"Previous ({previous_date.date()})"
    )

    # Titles
    ax.set_title(
        f"{country} Yield Curve",
        fontsize=14
    )

    ax.set_xlabel("Maturity")
    ax.set_ylabel("Yield (%)")

    # Smaller legend
    ax.legend(fontsize=9)

    # Grid
    ax.grid(True)

    # Tight layout
    fig.tight_layout()

    return fig
