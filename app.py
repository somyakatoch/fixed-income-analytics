import streamlit as stimport pandas as pd

from fred_loader import (get_fred_client,fetch_country_data,build_current_previous_curve,SERIES_CODES)

from plotting import plot_yield_curve

from calculations import (calculate_spread,classify_curve,macro_interpretation)

st.set_page_config(page_title="Global Yield Curve Dashboard",page_icon="📈",layout="wide")

st.title("📈 Global Yield Curve Dashboard")st.caption("Real FRED data for US, Japan, Australia, and New Zealand")

=========================

SIDEBAR

=========================

st.sidebar.header("Dashboard Controls")

country = st.sidebar.selectbox("Select country",list(SERIES_CODES.keys()))

st.sidebar.subheader("Date Selection")

date_mode = st.sidebar.radio("Select comparison mode",["Previous Months","Custom Dates"])

if date_mode == "Previous Months":months_back = st.sidebar.slider("Compare with how many months ago?",min_value=1,max_value=24,value=1)

custom_dates = False

else:custom_dates = True

current_date_input = st.sidebar.date_input(
    "Current Curve Date"
)

previous_date_input = st.sidebar.date_input(
    "Comparison Curve Date"
)

=========================

FRED API KEY

=========================

try:api_key = st.secrets["FRED_API_KEY"]except Exception:api_key = ""

if not api_key:api_key = st.sidebar.text_input("Enter FRED API Key",type="password")

if not api_key:st.warning("Please enter your FRED API key in the sidebar.")st.stop()

=========================

MAIN APP

=========================

try:fred = get_fred_client(api_key)

with st.spinner("Fetching real FRED data..."):

    country_data = fetch_country_data(fred, country)

    if custom_dates:

        latest_date = pd.to_datetime(current_date_input)
        previous_date = pd.to_datetime(previous_date_input)

        maturities = list(country_data.keys())

        current_curve = []
        previous_curve = []

        for maturity in maturities:

            series = country_data[maturity]

            current_value = series.loc[:latest_date].iloc[-1]
            previous_value = series.loc[:previous_date].iloc[-1]

            current_curve.append(float(current_value))
            previous_curve.append(float(previous_value))

        curve_data = {
            "maturities": maturities,
            "latest_date": latest_date,
            "previous_date": previous_date,
            "current_curve": current_curve,
            "previous_curve": previous_curve
        }

    else:

        curve_data = build_current_previous_curve(
            country_data,
            months_back=months_back
        )

# =========================
# CALCULATIONS
# =========================

current_spread = calculate_spread(curve_data["current_curve"])
previous_spread = calculate_spread(curve_data["previous_curve"])

spread_change = current_spread - previous_spread

# =========================
# METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

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
        "Spread Change",
        f"{spread_change:.2f}%"
    )

with col4:
    st.metric(
        "Curve Type",
        classify_curve(current_spread)
    )

# =========================
# CHART
# =========================

st.subheader(f"{country}: Current vs Comparison Yield Curve")

fig = plot_yield_curve(country, curve_data)
st.pyplot(fig, use_container_width=False)

# =========================
# DATA TABLE
# =========================

st.subheader("Real Data Table")

current_col = f"Current ({curve_data['latest_date'].date()})"
previous_col = f"Comparison ({curve_data['previous_date'].date()})"

table = pd.DataFrame({
    "Maturity": curve_data["maturities"],
    current_col: curve_data["current_curve"],
    previous_col: curve_data["previous_curve"]
})

table["Change"] = table[current_col] - table[previous_col]

st.dataframe(
    table,
    use_container_width=True
)

# =========================
# INTERPRETATION
# =========================

st.subheader("Interpretation")
st.write(macro_interpretation(current_spread))

st.markdown("---")

# =========================
# SERIES USED
# =========================

st.subheader("FRED Series Used")

series_table = pd.DataFrame([
    {
        "Country": country,
        "Maturity": maturity,
        "FRED Series Code": code
    }
    for maturity, code in SERIES_CODES[country].items()
])

st.dataframe(
    series_table,
    use_container_width=True
)

except Exception as e:st.error("Something went wrong.")st.exception(e)
