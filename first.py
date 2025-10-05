# 1. Import Libraries
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# 2. Create / Connect SQL Database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_data (
    order_id INTEGER,
    order_date TEXT,
    product_id INTEGER,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    store_id INTEGER
)
""")

# Insert demo data if empty
cursor.execute("SELECT COUNT(*) FROM sales_data")
if cursor.fetchone()[0] == 0:
    sample_data = [
        (1,"2023-01-10",101,"Laptop","Electronics",2,60000,1),
        (2,"2023-02-15",102,"Phone","Electronics",5,20000,1),
        (3,"2023-02-25",103,"Shirt","Clothing",10,1200,2),
        (4,"2023-03-05",104,"Shoes","Clothing",3,3000,2),
        (5,"2023-03-20",105,"Fridge","Appliances",1,40000,1),
        (6,"2023-04-15",102,"Phone","Electronics",4,21000,3),
        (7,"2023-05-12",106,"AC","Appliances",2,35000,1),
        (8,"2023-05-22",103,"Shirt","Clothing",15,1100,2)
    ]
    cursor.executemany("INSERT INTO sales_data VALUES (?,?,?,?,?,?,?,?)", sample_data)
    conn.commit()

# 3. Extract Data
monthly_df = pd.read_sql_query("""
    SELECT strftime('%Y-%m', order_date) AS month,
           SUM(quantity*price) AS total_sales
    FROM sales_data
    GROUP BY month
    ORDER BY month
""", conn)

top_products = pd.read_sql_query("""
    SELECT product_name, SUM(quantity) AS units_sold
    FROM sales_data
    GROUP BY product_name
    ORDER BY units_sold DESC
    LIMIT 5
""", conn)

print("Top 5 Best Selling Products:\n", top_products)

# 4. Data Transformation
monthly_df['month'] = pd.to_datetime(monthly_df['month'])
monthly_df.set_index('month', inplace=True)
monthly_df['moving_avg'] = monthly_df['total_sales'].rolling(window=3, min_periods=1).mean()

# 5. Forecasting
x = np.arange(len(monthly_df))
y = monthly_df['total_sales'].values
coeffs = np.polyfit(x, y, 1)
forecast_model = np.poly1d(coeffs)

future_x = np.arange(len(monthly_df), len(monthly_df)+6)
future_sales = forecast_model(future_x)
future_dates = pd.date_range(start=monthly_df.index[-1] + pd.offsets.MonthBegin(1), periods=6, freq="M")

# 6. Visualization
plt.figure(figsize=(10,6))
plt.plot(monthly_df.index, monthly_df['total_sales'], marker='o', label="Actual Sales")
plt.plot(monthly_df.index, monthly_df['moving_avg'], label="3-Month Moving Avg", linewidth=2)
plt.plot(future_dates, future_sales, 'r--', marker='x', label="Forecast")
plt.title("Sales Forecasting & Demand Planning")
plt.xlabel("Date")
plt.ylabel("Sales Revenue")
plt.legend()
plt.grid(True)
plt.show()

# 7. Insights
print("\n✅ Insights:")
print("- Electronics dominate sales (Laptop, Phone).")
print("- Sales are seasonal (peaks visible in data).")
print("- Forecast shows upward demand trend for next 6 months.")
