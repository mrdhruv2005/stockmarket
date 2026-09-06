# Stock Market Dashboard

A Flask web app that fetches six months of daily price history for any stock ticker and
renders it as an interactive Plotly candlestick chart with 50-day and 200-day moving
averages overlaid.

---

## What it does

Enter a ticker (`AAPL`, `TSLA`, `RELIANCE.NS`, …) and the app:

1. Pulls six months of daily OHLC data from Yahoo Finance via `yfinance`
2. Computes 50-day and 200-day simple moving averages
3. Renders an interactive candlestick chart with both MAs overlaid
4. Displays the underlying data as an HTML table

### Why candlesticks and these two averages

A **candlestick** encodes four values per day — open, high, low, close — in a single mark,
so a trader can read intraday range and direction at a glance. A line chart of closing
prices discards three of those four numbers.

The **50-day and 200-day** windows are the two most widely watched moving averages in
technical analysis. The 50-day tracks intermediate trend; the 200-day tracks long-term
trend. Their crossings have conventional names (a "golden cross" when the 50 rises above
the 200, a "death cross" for the inverse), which is why these particular windows are the
useful defaults rather than arbitrary ones.

Note that with only six months (~126 trading days) of data, the 200-day average is
incomplete — `rolling(window=200)` produces `NaN` until enough history accumulates, so the
200-day line will not render for the earlier portion of the window. Fetching a longer
period would be needed for a complete 200-day trace.

---

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Ticker input form |
| `POST` | `/` | Fetch, compute, and render chart + table |
| `GET` | `/ping` | Health check — returns `OK` (200) |

The `/ping` endpoint exists so an external uptime monitor can keep a free-tier host awake
and alert on downtime, without loading the full page or hitting the Yahoo Finance API on
every check.

---

## Error handling

Ticker input is uppercased and stripped before use. If `yfinance` returns an empty frame —
which is what happens for a nonexistent or delisted symbol — the app reports
`No data found for ticker 'X'` rather than raising, and network or API failures are caught
and surfaced as a message instead of a stack trace.

---

## Running locally

```bash
git clone https://github.com/mrdhruv2005/stockmarket.git
cd stockmarket

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python app.py
```

Open `http://localhost:5000`. No API key required — `yfinance` scrapes public Yahoo
Finance endpoints.

---

## Repository structure

```
├── app.py                # Flask app: routing, data fetch, chart generation
├── templates/index.html  # Form, chart container, data table
└── requirements.txt
```

---

## Limitations

- **Fixed six-month window.** Period and interval are hardcoded; no user control over
  range or granularity.
- **Incomplete 200-day MA**, for the reason described above.
- **No caching.** Every submission re-fetches from Yahoo Finance, so repeated lookups of
  the same ticker are slower than necessary and burn API calls.
- **`yfinance` is unofficial.** It depends on undocumented Yahoo endpoints that change
  without notice; it can break with no warning.
- **No input validation beyond emptiness.** Any string is sent to the API.
- **Not investment advice.** Moving averages are descriptive indicators, not predictions.

---

## Tech stack

Python · Flask · yfinance · Plotly · Pandas
