def calculate_spread(curve):
    return curve[-1] - curve[0]


def classify_curve(spread):
    if spread > 0.75:
        return "Normal / Steep"
    elif spread > 0.10:
        return "Slightly Positive"
    elif spread >= -0.10:
        return "Flat"
    else:
        return "Inverted"


def macro_interpretation(spread):
    if spread > 0.75:
        return """
The yield curve is normal or steep.  
This usually means long-term yields are higher than short-term rates.

Possible meaning:
- markets expect future growth,
- inflation risk may still exist,
- central bank may not be expected to cut aggressively.
"""

    elif spread > 0.10:
        return """
The yield curve is mildly upward sloping.

Possible meaning:
- economy may be stable,
- markets are not pricing severe recession risk,
- policy may be near neutral.
"""

    elif spread >= -0.10:
        return """
The yield curve is flat.

Possible meaning:
- market is uncertain,
- policy may be near a turning point,
- investors are waiting for clearer growth or inflation signals.
"""

    else:
        return """
The yield curve is inverted.

Possible meaning:
- short-term rates are higher than long-term yields,
- markets may expect future rate cuts,
- growth slowdown or recession risk may be rising.
"""
