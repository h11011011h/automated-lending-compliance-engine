import pandas as pd
import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect("lending_data.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, customer_name TEXT, loan_amount REAL, fees REAL, risk_score INTEGER)")
cursor.executemany("INSERT OR REPLACE INTO transactions VALUES (?,?,?,?,?)", [(1, 'John Doe', 12000.0, 250.0, 40), (2, 'Jane Smith', 500.0, 125.0, 20)])
conn.commit()

df = pd.read_sql_query("SELECT * FROM transactions", conn)
df['AML_Flag'] = df['loan_amount'] >= 10000
df['UDAAP_Risk'] = (df['fees'] / df['loan_amount']) > 0.15

if not os.path.exists("reports"): os.makedirs("reports")
df.to_excel("reports/Audit_Report.xlsx", index=False)
conn.close()
print("--- SUCCESS: Audit Complete ---")
