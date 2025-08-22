from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    graphJSON = None
    table_html = None
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker").upper().strip()

        try:
            # Fetch stock data (last 6 months for better candlestick view)
            data = yf.download(ticker, period="6mo", interval="1d")
            if data.empty:
                error = f"No data found for ticker '{ticker}'."
            else:
                # Moving Averages
                data["MA50"] = data["Close"].rolling(window=50).mean()
                data["MA200"] = data["Close"].rolling(window=200).mean()

                # Create candlestick chart
                fig = go.Figure()

                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="Candlesticks"
                ))

                # Add moving averages
                fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], line=dict(color='blue', width=1.5), name="50-Day MA"))
                fig.add_trace(go.Scatter(x=data.index, y=data["MA200"], line=dict(color='orange', width=1.5), name="200-Day MA"))

                # Add volume bars
                fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume", yaxis="y2", opacity=0.3))

                # Layout adjustments
                fig.update_layout(
                    title=f"{ticker} Stock Price (Candlestick + Volume)",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    template="plotly_dark",
                    yaxis2=dict(
                        overlaying='y',
                        side='right',
                        showgrid=False,
                        title="Volume"
                    ),
                    xaxis_rangeslider_visible=False
                )

                graphJSON = fig.to_html(full_html=False)

                # Show last 10 days in a table
                table_html = data.tail(10).to_html(classes="table table-striped table-bordered")

        except Exception as e:
            error = str(e)

    return render_template("index.html", graphJSON=graphJSON, table_html=table_html, error=error)


if __name__ == "__main__":
    app.run(debug=True)
