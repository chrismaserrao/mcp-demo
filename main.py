from fastmcp import FastMCP
from database import init_db, insert_transaction, get_transactions_df

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from prophet import Prophet

mcp = FastMCP("Finance-Agent")

# Initialize database on startup
init_db()


# =============================
# TOOL 1: Add Transaction
# =============================
@mcp.tool()
def add_transaction(
    user_id: str,
    date: str,
    description: str,
    amount: float,
    transaction_type: str,
    category: str,
    account_name: str
) -> str:
    """
    Adds a transaction to the database.
    """

    insert_transaction(
        user_id,
        date,
        description,
        amount,
        transaction_type.lower(),
        category,
        account_name
    )

    return "Transaction successfully added."


# =============================
# TOOL 2: Spending Summary
# =============================
@mcp.tool()
def get_spending_summary(user_id: str) -> str:
    """
    Returns income, expenses, and net savings.
    """

    df = get_transactions_df(user_id)

    if df.empty:
        return "No transactions found."

    income = df[df["transaction_type"] == "credit"]["amount"].sum()
    expenses = df[df["transaction_type"] == "debit"]["amount"].sum()

    savings = income - expenses

    return (
        f"Total Income: {income}\n"
        f"Total Expenses: {expenses}\n"
        f"Net Savings: {savings}"
    )


# =============================
# TOOL 3: Financial Personality (ML)
# =============================
@mcp.tool()
def analyze_financial_personality(user_id: str) -> str:
    """
    Uses clustering to determine financial personality.
    """

    df = get_transactions_df(user_id)

    if df.empty:
        return "Not enough data."

    income = df[df["transaction_type"] == "credit"]["amount"].sum()
    expenses = df[df["transaction_type"] == "debit"]["amount"].sum()

    if income == 0:
        return "No income data."

    savings_ratio = (income - expenses) / income
    avg_transaction = df["amount"].mean()
    volatility = df["amount"].std() if len(df) > 1 else 0

    features = np.array([[savings_ratio, avg_transaction, volatility]])

    # Train dummy model (for MVP)
    dummy_data = np.random.rand(50, 3)
    model = KMeans(n_clusters=3, random_state=42)
    model.fit(dummy_data)

    cluster = model.predict(features)[0]

    mapping = {
        0: "Conservative Saver",
        1: "Balanced Planner",
        2: "Aggressive Spender"
    }

    return f"Financial Personality: {mapping.get(cluster, 'Unknown')}"


# =============================
# TOOL 4: Cash Flow Forecast (ML)
# =============================
@mcp.tool()
def forecast_next_month(user_id: str) -> str:
    """
    Forecasts next month cash flow using Prophet.
    """

    df = get_transactions_df(user_id)

    if df.empty:
        return "Not enough data to forecast."

    df["date"] = pd.to_datetime(df["date"])

    monthly = df.groupby(pd.Grouper(key="date", freq="M"))["amount"].sum().reset_index()

    if len(monthly) < 2:
        return "Need at least 2 months of data."

    monthly.columns = ["ds", "y"]

    model = Prophet()
    model.fit(monthly)

    future = model.make_future_dataframe(periods=1, freq="M")
    forecast = model.predict(future)

    next_month = forecast.iloc[-1]["yhat"]

    return f"Predicted net cash flow next month: {round(next_month, 2)}"


# =============================
# TOOL 5: Risk Alert (Rule-Based)
# =============================
@mcp.tool()
def risk_alert(user_id: str) -> str:
    """
    Simple rule-based financial risk alert.
    """

    df = get_transactions_df(user_id)

    if df.empty:
        return "No data available."

    income = df[df["transaction_type"] == "credit"]["amount"].sum()
    expenses = df[df["transaction_type"] == "debit"]["amount"].sum()

    if income == 0:
        return "No income data."

    savings_ratio = (income - expenses) / income

    if savings_ratio < 0.05:
        return "⚠️ High financial risk: Savings below 5%."
    else:
        return "No major financial risk detected."


# =============================
# RUN SERVER
# =============================
if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000
    )
