# Global Yield Curve Dashboard

Interactive Streamlit dashboard for analysing real yield curve data using FRED.

## Countries Covered

- United States
- Japan
- Australia
- New Zealand

## What the Dashboard Shows

The dashboard compares:

- 1D / policy-rate proxy
- 10-year government bond yield
- Current value
- Previous month value
- Yield spread
- Curve shape interpretation

## Repository Structure

```text
global-yield-curve-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── fred_loader.py
│   ├── plotting.py
│   └── calculations.py
│
├── data/
├── assets/
└── .streamlit/
    └── secrets.toml
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

## FRED API Key

Create a file:

```text
.streamlit/secrets.toml
```

Add:

```toml
FRED_API_KEY = "your_fred_api_key_here"
```

## Data Sources

The dashboard uses FRED series for policy/short-rate proxies and 10-year government bond yields.

## Important Note

This dashboard currently shows a real 1D / policy-rate proxy to 10Y comparison. A full multi-maturity curve for all countries would require additional real series for 1M, 3M, 6M, 1Y, 2Y, 5Y, and 10Y for each country.
