import yfinance as yf
import pandas as pd
import numpy as np
import db_helper_stock as db
import warnings
warnings.filterwarnings('ignore')


def fetch_stock_data(ticker: str, period: str = "1y"):
    """
    Fetch stock data from Yahoo Finance and return a cleaned DataFrame.
    """
    df = yf.download(ticker, period=period, interval="1d")

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        df.columns.name = None

    # Make Date a column
    df.reset_index(inplace=True)

    # Sort by date
    df.sort_values("Date", inplace=True)

    return df


def validate_data(df: pd.DataFrame):
    """
    Print basic data quality checks.
    """
    print("Null values:\n", df.isnull().sum())
    print("Duplicate rows:", df.duplicated().sum())


def add_financial_metrics(df: pd.DataFrame):
    """
    Add Daily Return and 7-day Moving Average.
    """
    df["Daily_Return"] = (df["Close"] - df["Open"]) / df["Open"]
    df["MA_7"] = df["Close"].rolling(7).mean()
    median_ma7 = df["MA_7"].median()

    df["MA_7"].fillna(median_ma7, inplace=True)

    return df

def calculate_52_week_high_low(df: pd.DataFrame):
    """
    Return 52-week high and low prices.
    """
    high_52 = df["High"].max()
    low_52 = df["Low"].min()
    return high_52, low_52

def calculate_volatility(df: pd.DataFrame):
    """
    Calculate volatility as std deviation of daily returns.
    """
    return df["Daily_Return"].std()


def calculate_correlation(ticker1: str, ticker2: str, period: str = "1y"):
    """
    Calculate correlation between closing prices of two stocks.
    """

    # Download data
    stock1 = yf.download(ticker1, period=period, interval="1d")
    stock2 = yf.download(ticker2, period=period, interval="1d")

    # Flatten columns if MultiIndex
    if isinstance(stock1.columns, pd.MultiIndex):
        stock1.columns = stock1.columns.get_level_values(0)
        stock1.columns.name = None

    if isinstance(stock2.columns, pd.MultiIndex):
        stock2.columns = stock2.columns.get_level_values(0)
        stock2.columns.name = None

    # Keep only Close prices
    stock1 = stock1[["Close"]].rename(columns={"Close": ticker1})
    stock2 = stock2[["Close"]].rename(columns={"Close": ticker2})

    # Align by date (inner join)
    merged = stock1.join(stock2, how="inner")

    # Compute correlation
    correlation = merged[ticker1].corr(merged[ticker2])

    return correlation




if __name__ == "__main__":

    TICKERS = ["INFY.NS", "TCS.NS"]

    for TICKER in TICKERS:
        print(f"\nProcessing {TICKER}")

        df = fetch_stock_data(TICKER)
        validate_data(df)

        df = add_financial_metrics(df)

        high_52, low_52 = calculate_52_week_high_low(df)
        print(f"{TICKER} 52-Week High: {high_52}")
        print(f"{TICKER} 52-Week Low: {low_52}")

        volatility = calculate_volatility(df)
        print(f"{TICKER} Volatility Score: {volatility}")

        print(df.head())

        # ---- DB INSERTION ----
        db.insert_company(TICKER)
        company_id = db.get_company_id(TICKER)

        for _, row in df.iterrows():
            db.insert_stock_data(company_id, row)

        print(f"{TICKER} data stored successfully")

    # ---- OPTIONAL: CORRELATION CHECK ----
    correlation = calculate_correlation("INFY.NS", "TCS.NS")
    print("\nINFY vs TCS Correlation:", correlation)
