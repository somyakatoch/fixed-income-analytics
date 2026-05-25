from fredapi import Fred
import pandas as pd


SERIES_CODES = {
    "US": {
        "1D / Policy": "DFF",
        "10Y": "DGS10"
    },
    "Japan": {
        "1D / Policy": "IRSTCI01JPM156N",
        "10Y": "IRLTLT01JPM156N"
    },
    "Australia": {
        "1D / Policy": "IRSTCI01AUM156N",
        "10Y": "IRLTLT01AUM156N"
    },
    "New Zealand": {
        "1D / Policy": "IRSTCI01NZM156N",
        "10Y": "IRLTLT01NZM156N"
    }
}


def get_fred_client(api_key: str) -> Fred:
    if not api_key:
        raise ValueError("Missing FRED API key.")
    return Fred(api_key=api_key)


def fetch_country_data(fred: Fred, country: str) -> dict:
    if country not in SERIES_CODES:
        raise ValueError(f"Country not supported: {country}")

    country_data = {}

    for maturity, code in SERIES_CODES[country].items():
        series = fred.get_series(code)
        series = series.dropna()
        series.index = pd.to_datetime(series.index)
        country_data[maturity] = series

    return country_data


def build_current_previous_curve(country_data: dict, months_back: int = 1) -> dict:
    maturities = list(country_data.keys())

    latest_date = min(series.index.max() for series in country_data.values())
    previous_target_date = latest_date - pd.DateOffset(months=months_back)

    current_curve = []
    previous_curve = []

    for maturity in maturities:
        series = country_data[maturity]

        current_value = series.loc[:latest_date].iloc[-1]
        previous_value = series.loc[:previous_target_date].iloc[-1]

        current_curve.append(float(current_value))
        previous_curve.append(float(previous_value))

    return {
        "maturities": maturities,
        "latest_date": latest_date,
        "previous_date": previous_target_date,
        "current_curve": current_curve,
        "previous_curve": previous_curve
    }
