# Stock Market Dashboard – Take-Home Assignment

## Overview

This project is a full-stack **stock market dashboard** that demonstrates.

The goal of this assignment was to:
- Data collection and preprocessing
- Relational database design
- REST API development
- Interactive data visualization
- Basic machine learning integration
---

## What Was Implemented

### 1. Data & Analytics
- Fetch daily stock data using Yahoo Finance
- Clean and preprocess data with Pandas
- Compute financial metrics:
  - Daily Return
  - 7-Day Moving Average
  - 52-Week High & Low
  - Volatility (risk)

---

### 2. Backend APIs (FastAPI)

- List available companies
- Fetch recent stock prices
- Summary statistics per stock
- Compare two stocks
- Identify Top Gainers / Losers
- Predict future prices using ML

---
### 3.Visualization Dashboard

- Company list sidebar
- Interactive line chart (Chart.js)
- Filters: Last 30 / 90 days
- Market insights: Top Gainers & Losers
- ML prediction line (dashed)
---


### 4. Machine Learning

- Linear Regression–based price prediction
- Time-index feature to avoid data leakage
- Demonstrates ML integration (not financial advice)

---
### 5.Tech Stack
- Language:	Python
- Backend:	FastAPI
- Database:	MySQL
- Data Processing:	Pandas, NumPy
- ML:	Scikit-learn
- Frontend:	HTML, CSS, JavaScript
- Charts:	Chart.js
- APIs Docs:	Swagger (FastAPI)
- Version Control:	Git & GitHub
---
### folder structure

```
 stock_dashboard/
│
├── frontend/
│   └── index.html
│
├── scripts/
│   ├── part1_data_collection_cleaning.py
│   ├── db_helper_stock.py
│   └── server_stock.py
│
├── .env            # NOT committed
├── .gitignore
├── README.md
└── requirements.txt

```


--- 


### Setup Instructions (Step-by-Step)
```
git clone https://github.com/sanketdev1234/stock-dashboard-fastapi.git
cd stock-dashboard-fastapi
```
## How to Run the Project
- Create Virtual Environment
  ```
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
  ```

### Install Dependencies
```
 pip install -r requirements.txt
```

### requirements.txt
```
fastapi
uvicorn
pandas
numpy
yfinance
mysql-connector-python
python-dotenv
scikit-learn

```

### Setup MySQL Database
```
CREATE DATABASE stock_dashboard;
USE stock_dashboard;

CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE stock_prices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id INT,
    trade_date DATE,
    open_price DOUBLE,
    high_price DOUBLE,
    low_price DOUBLE,
    close_price DOUBLE,
    volume BIGINT,
    daily_return DOUBLE,
    ma_7 DOUBLE,
    UNIQUE (company_id, trade_date),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

```

### Environment Variables
```
HOST=localhost
USER=root
PASSWORD=your_password
DATABASE=stock_dashboard
```
### Run Data Ingestion Pipeline
```
python scripts/part1_data_collection_cleaning.py
```
### Run Data Ingestion Pipeline
```
uvicorn scripts.server_stock:app --reload
 
API Docs(Swagger):
http://127.0.0.1:8000/docs

 Open Dashboard
 Open in browser:
  frontend/index.html

 API Endpoints:

  Companies
GET /companies

  Stock Data
GET /data/{ticker}

  Summary
GET /summary/{ticker}

  Compare Two Stocks
GET /compare?symbol1=INFY.NS&symbol2=TCS.NS

  Top Gainers / Losers
GET /insights/top-movers

  Price Prediction (ML)
GET /predict/{ticker}?days=5
```

### Machine Learning Explanation
- Why Linear Regression?
  - Simple and interpretable
  - Suitable for trend demonstration
  - Easy to integrate in APIs

- Feature Choice?
  - Uses time index as input
  - Avoids data leakage (future OHLC values are unknown)
---

### Dashboard Explanation

- Sidebar loads companies dynamically

- Clicking a company updates the chart

- Filters adjust visible time range

- Gainers/Losers show market insights

- Prediction line visualizes future trend
---
### Data Integrity & Best Practices

- Database-level unique constraints

- Idempotent inserts (INSERT IGNORE)

- .env excluded via .gitignore

- Swagger for self-documenting APIs

---
---

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/aac01426-8425-4c1f-b37d-da40a48bb57e" />
---

<img width="531" height="153" alt="image" src="https://github.com/user-attachments/assets/aee1b3a5-8fa8-411d-970c-24ca12c73e4a" />
---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fe0c370b-80c2-441a-9c30-98462a1de60f" />
---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4be7cbb9-d1e5-468e-af33-1bdebffe3be4" />
---












