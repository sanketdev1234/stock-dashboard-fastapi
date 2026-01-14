from fastapi import FastAPI, HTTPException
import db_helper_stock as db
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI(title="Stock Data API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/companies")
def get_companies():
    return db.fetch_companies()

@app.get("/data/{ticker}")
def get_stock_data(ticker: str):
    return db.fetch_stock_data_days(ticker, limit=120)


@app.get("/summary/{ticker}")
def get_stock_summary(ticker: str):
    summary = db.fetch_summary(ticker)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@app.get("/compare")
def compare_stocks(symbol1: str, symbol2: str):


    data = db.compare_stocks(symbol1, symbol2)

    if not data or len(data) < 2:
        raise HTTPException(
            status_code=404,
            detail="One or both stock symbols not found"
        )

    result = {}
    for row in data:
        result[row["ticker"]] = {
            "average_close_price": row["avg_close"],
            "average_daily_return": row["avg_daily_return"],
            "volatility": row["volatility"]
        }

    return {
        "comparison": result,
        "insight": "Higher average return with lower volatility indicates better risk-adjusted performance"
    }

@app.get("/insights/top-movers")
def top_movers():
    return db.fetch_top_gainers_losers()


@app.get("/predict/{ticker}")
def predict_stock_price(ticker: str, days: int = 5):
    """
    Predict next `days` closing prices using Linear Regression
    """

    # Fetch historical data (use existing helper)
    data = db.fetch_stock_data_days(ticker, limit=60)

    if not data or len(data) < 10:
        raise HTTPException(status_code=400, detail="Not enough data for prediction")

    # Prepare training data
    prices = [row["close_price"] for row in data][::-1]

    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future
    future_X = np.arange(len(prices), len(prices) + days).reshape(-1, 1)
    predictions = model.predict(future_X)

    return {
        "historical": prices,
        "predicted": predictions.tolist()
    }


