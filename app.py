import streamlit as st
import pandas as pd

from fred_loader import (
    get_fred_client,
    fetch_country_data,
    build_current_previous_curve,
    SERIES_CODES
)

from plotting import plot_yield_curve

from calculations import (
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

# FRED API key
try:
    api_key = st.secrets["FRED_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    api_key = st.sidebar.text_input(
        "Enter FRED API Key",
        type="password"
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

    current_col = f"Current ({curve_data['latest_date'].date()})"
    previous_col = f"Previous ({curve_data['previous_date'].date()})"

    table = pd.DataFrame({
        "Maturity": curve_data["maturities"],
        current_col: curve_data["current_curve"],
        previous_col: curve_data["previous_curve"]
    })

    table["Change"] = table[current_col] - table[previous_col]

    st.dataframe(table, use_container_width=True)

    st.subheader("Interpretation")
    st.write(macro_interpretation(current_spread))

    st.markdown("---")

    st.subheader("FRED Series Used")

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
