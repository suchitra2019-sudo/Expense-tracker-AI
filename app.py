import sqlite3
import streamlit as st
import pandas as pd
from datetime import date

# ---------------- DB ----------------
conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)''')

# ---------------- CATEGORY ----------------
def categorize(text):
    text = text.lower()
    if "lunch" in text or "dinner" in text:
        return "Food"
    elif "uber" in text or "petrol" in text:
        return "Travel"
    elif "bill" in text:
        return "Bills"
    else:
        return "Other"

# ---------------- UI ----------------
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker")

menu = st.sidebar.selectbox("Menu", ["Add Expense", "Dashboard"])

# ---------------- ADD ----------------
if menu == "Add Expense":
    st.subheader("➕ Add Expense")

    expense_date = st.date_input("Date", date.today())
    amount = st.number_input("Amount", min_value=0.0)
    description = st.text_input("Description")

    if st.button("Add"):
        category = categorize(description) if description else "Other"

        c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                  (str(expense_date), category, amount, description))
        conn.commit()

        st.success(f"Added ₹{amount} under {category}")

# ---------------- DASHBOARD ----------------
else:
    st.subheader("📊 Dashboard")

    df = pd.read_sql_query("SELECT * FROM expenses", conn)

    if df.empty:
        st.warning("No data yet")
    else:
        df['date'] = pd.to_datetime(df['date'])

        st.metric("Total Spend", f"₹{df['amount'].sum()}")

        st.bar_chart(df.groupby('category')['amount'].sum())

        st.dataframe(df)
