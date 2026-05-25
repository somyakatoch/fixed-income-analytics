def calculate_spread(curve: list) -> float:
    """
    For current setup:
    curve[0] = 1D / Policy rate
    curve[1] = 10Y yield
    Spread = 10Y - 1D
    """
    if len(curve) < 2:
        return None
    return curve[1] - curve[0]


def classify_curve(spread: float) -> str:
    if spread is None:
        return "Not enough data"

    if spread > 0.50:
        return "Normal / upward sloping"
    elif 0 <= spread <= 0.50:
        return "Nearly flat"
    else:
        return "Inverted"


def macro_interpretation(spread: float) -> str:
    if spread is None:
        return "Not enough data to interpret."

    if spread > 0.50:
        return (
            "The curve is upward sloping. This usually suggests markets expect "
            "normal growth conditions, with long-term yields above short-term rates."
        )
    elif 0 <= spread <= 0.50:
        return (
            "The curve is almost flat. This can mean markets are uncertain about "
            "future growth, inflation, or central bank policy direction."
        )
    else:
        return (
            "The curve is inverted. Short-term/policy rates are above long-term yields, "
            "which often signals restrictive monetary policy and expectations of future rate cuts."
        )
