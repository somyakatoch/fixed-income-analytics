import streamlit as st
import pandas as pd

from utils.fred_loader import (
    get_fred_client,
    fetch_country_data,
    build_current_previous_curve,
    SERIES_CODES
)
from utils.plotting import plot_yield_curve
from utils.calculations import (
    calculate_spread,
    classify_curve,
    macro_interpretation
)


st.set_page_config(
    page_title="Global Yield Curve Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Global Yield Curve Dashboard")
st.caption("Real FRED data for US, Japan, Australia, and New Zealand")

st.sidebar.header("Dashboard Controls")

country = st.sidebar.selectbox(
    "Select country",
    list(SERIES_CODES.keys())
)

months_back = st.sidebar.slider(
    "Compare with how many months ago?",
    min_value=1,
    max_value=12,
    value=1
)

st.sidebar.markdown("---")

api_key = st.secrets.get("FRED_API_KEY", "")

if not api_key or api_key == "PASTE_YOUR_FRED_API_KEY_HERE":
    api_key = st.sidebar.text_input(
        "Enter FRED API Key",
        type="password"
    )

st.sidebar.info(
    "For deployment, save your FRED key in Streamlit Secrets as FRED_API_KEY."
)

if not api_key:
    st.warning("Please enter your FRED API key in the sidebar.")
    st.stop()

try:
    fred = get_fred_client(api_key)

    with st.spinner("Fetching real FRED data..."):
        country_data = fetch_country_data(fred, country)
        curve_data = build_current_previous_curve(
            country_data,
            months_back=months_back
        )

    current_spread = calculate_spread(curve_data["current_curve"])
    previous_spread = calculate_spread(curve_data["previous_curve"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current 10Y - 1D Spread",
            f"{current_spread:.2f}%"
        )

    with col2:
        st.metric(
            "Previous Spread",
            f"{previous_spread:.2f}%"
        )

    with col3:
        st.metric(
            "Curve Type",
            classify_curve(current_spread)
        )

    st.subheader(f"{country}: Current vs Previous Yield Curve")

    fig = plot_yield_curve(country, curve_data)
    st.pyplot(fig)

    st.subheader("Real Data Table")

    table = pd.DataFrame({
        "Maturity": curve_data["maturities"],
        f"Current ({curve_data['latest_date'].date()})": curve_data["current_curve"],
        f"Previous ({curve_data['previous_date'].date()})": curve_data["previous_curve"]
    })

    table["Change"] = (
        table[f"Current ({curve_data['latest_date'].date()})"]
        - table[f"Previous ({curve_data['previous_date'].date()})"]
    )

    st.dataframe(table, use_container_width=True)

    st.subheader("Interpretation")
    st.write(macro_interpretation(current_spread))

    st.markdown("---")
    st.subheader("Series Used")

    series_table = pd.DataFrame([
        {
            "Country": country,
            "Maturity": maturity,
            "FRED Series Code": code
        }
        for maturity, code in SERIES_CODES[country].items()
    ])

    st.dataframe(series_table, use_container_width=True)

except Exception as e:
    st.error("Something went wrong.")
    st.exception(e)
