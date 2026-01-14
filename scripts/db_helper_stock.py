import os
import mysql.connector
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DB_HOST = os.getenv("HOST")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DATABASE")


@contextmanager
def get_db_connection(commit=False):
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def insert_company(ticker: str):
    with get_db_connection(commit=True) as cursor:
        cursor.execute(
            "INSERT IGNORE INTO companies (ticker) VALUES (%s)",
            (ticker,)
        )


def get_company_id(ticker: str):
    with get_db_connection() as cursor:
        cursor.execute(
            "SELECT id FROM companies WHERE ticker = %s",
            (ticker,)
        )
        result = cursor.fetchone()
        return result["id"] if result else None



def insert_stock_data(company_id: int, row: dict):
    with get_db_connection(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO stock_prices (
                company_id, trade_date, open_price, high_price,
                low_price, close_price, volume, daily_return, ma_7
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                company_id,
                row["Date"],
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
                row["Volume"],
                row["Daily_Return"],
                row["MA_7"]
            )
        )


def fetch_companies():
    with get_db_connection() as cursor:
        cursor.execute("SELECT ticker FROM companies")
        return cursor.fetchall()


def fetch_stock_data_days(ticker: str, limit: int = 120):
    with get_db_connection() as cursor:
        cursor.execute(
            """
            SELECT trade_date, close_price, ma_7
            FROM stock_prices
            WHERE company_id = (
                SELECT id FROM companies WHERE ticker = %s
            )
            ORDER BY trade_date DESC
            LIMIT %s
            """,
            (ticker, limit)
        )
        return cursor.fetchall()


def fetch_summary(ticker: str):
    with get_db_connection() as cursor:
        cursor.execute(
            """
            SELECT
                MAX(high_price) AS high_52,
                MIN(low_price) AS low_52,
                AVG(close_price) AS avg_close
            FROM stock_prices
            WHERE company_id = (
                SELECT id FROM companies WHERE ticker = %s
            )
            """,
            (ticker,)
        )
        return cursor.fetchone()


def compare_stocks(symbol1: str, symbol2: str):
    with get_db_connection() as cursor:
        query = """
        SELECT
            c.ticker,
            AVG(sp.close_price) AS avg_close,
            AVG(sp.daily_return) AS avg_daily_return,
            STDDEV(sp.daily_return) AS volatility
        FROM stock_prices sp
        JOIN companies c ON sp.company_id = c.id
        WHERE c.ticker IN (%s, %s)
        GROUP BY c.ticker;
        """
        cursor.execute(query, (symbol1, symbol2))
        return cursor.fetchall()



def fetch_top_gainers_losers(limit=5):
    with get_db_connection() as cursor:

        # Latest trading date
        cursor.execute("SELECT MAX(trade_date) AS latest FROM stock_prices")
        latest_date = cursor.fetchone()["latest"]

        # Top Gainers
        cursor.execute(
            """
            SELECT c.ticker, sp.daily_return
            FROM stock_prices sp
            JOIN companies c ON sp.company_id = c.id
            WHERE sp.trade_date = %s
            ORDER BY sp.daily_return DESC
            LIMIT %s
            """,
            (latest_date, limit)
        )
        gainers = cursor.fetchall()

        # Top Losers
        cursor.execute(
            """
            SELECT c.ticker, sp.daily_return
            FROM stock_prices sp
            JOIN companies c ON sp.company_id = c.id
            WHERE sp.trade_date = %s
            ORDER BY sp.daily_return ASC
            LIMIT %s
            """,
            (latest_date, limit)
        )
        losers = cursor.fetchall()

        return {
            "date": latest_date,
            "gainers": gainers,
            "losers": losers
        }


