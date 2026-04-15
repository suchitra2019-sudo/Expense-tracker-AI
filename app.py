import sqlite3
from datetime import date
from twilio.twiml.messaging_response import MessagingResponse

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


def whatsapp_bot():
    msg = request.form.get("Body")
    amount = [int(s) for s in msg.split() if s.isdigit()]

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

if __name__ == "__main__":
    app.run(port=5000)
