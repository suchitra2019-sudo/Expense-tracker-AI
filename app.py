import sqlite3
from datetime import date

# DB
conn = sqlite3.connect("expenses.db", check_same_thread=False)
c = conn.cursor()

# Categorization
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


    

    resp = MessagingResponse()

    if amount:
        amt = amount[0]
        category = categorize(msg)

        c.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                  (str(date.today()), category, amt, msg))
        conn.commit()

        resp.message(f"✅ Added ₹{amt} under {category}")
    else:
        resp.message("❌ Please send like: 'Spent 200 on food'")

    return str(resp)


    
