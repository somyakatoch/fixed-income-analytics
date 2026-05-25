import matplotlib.pyplot as plt


def plot_yield_curve(country: str, curve_data: dict):
    maturities = curve_data["maturities"]
    current_curve = curve_data["current_curve"]
    previous_curve = curve_data["previous_curve"]
    latest_date = curve_data["latest_date"]
    previous_date = curve_data["previous_date"]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        maturities,
        current_curve,
        marker="o",
        linewidth=3,
        label=f"Current ({latest_date.date()})"
    )

    ax.plot(
        maturities,
        previous_curve,
        linestyle="--",
        marker="x",
        linewidth=2.5,
        label=f"Previous ({previous_date.date()})"
    )

    ax.set_title(f"{country} Yield Curve: 1D / Policy Rate → 10Y")
    ax.set_xlabel("Maturity")
    ax.set_ylabel("Yield (%)")
    ax.grid(True)
    ax.legend()

    return fig
