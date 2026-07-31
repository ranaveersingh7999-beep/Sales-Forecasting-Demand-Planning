# 📈 Sales Forecasting & Demand Planning

---

### 🚀 Overview
This project builds a lightweight, end-to-end pipeline to analyze historical sales data stored in a local **SQLite** database and forecast future revenue trends. It uses SQL for aggregation, Pandas for time-series transformation, and a simple **linear regression trendline** (via NumPy) to project sales for the next 6 months — helping visualize demand direction at a glance.

The script is self-contained: it creates the database and seeds it with sample transactional data automatically if none exists, so it runs out of the box with no external files required.

---

### 🛠️ Tech Stack
* **Python**
* **Pandas & NumPy**
* **SQLite3** (embedded relational database)
* **Matplotlib** (visualization)

---

### ⚙️ Features
* **Self-seeding SQLite database** — creates `sales_data` table and inserts demo records if the table is empty
* **SQL-based analytics** — monthly revenue aggregation and top-5 best-selling products, computed directly via SQL queries
* **Time-series feature engineering** — converts monthly totals into a datetime-indexed series with a 3-month rolling moving average
* **Linear trend forecasting** — fits a first-degree polynomial (`np.polyfit`) to historical monthly sales and projects the next 6 months
* **Visualization** — single combined chart showing actual sales, moving average, and forecast

---

### 📊 Outputs
#### 🔹 Analysis
* **Top 5 best-selling products** (printed to console, ranked by units sold)
* **Monthly total sales** aggregated from raw order-level transactions

#### 🔹 Forecast
* **6-month sales forecast** based on a linear trendline fit to historical monthly revenue

#### 🔹 Visualizations
* **Sales trend chart** — actual monthly sales, 3-month moving average, and forecasted sales (dashed line) plotted together

---

### 📂 Project Structure
* `sales.db` — SQLite database file (auto-created on first run)
* `sales_forecasting.py` — Main script: database setup, SQL analytics, forecasting, and visualization

---

### ▶️ Running the Script
```bash
python sales_forecasting.py
```
On first run, the script creates `sales.db` and populates it with 8 sample orders across Electronics, Clothing, and Appliances categories. Subsequent runs reuse the existing database.

---

### 📝 Notes / Next Steps
* The linear trend model is intentionally simple (straight-line fit) — for more realistic forecasts, consider seasonal models (e.g. `statsmodels` SARIMA/ETS) once more historical data is available.
* Currently there's no `region` or `category`-level forecast breakdown — the trend is fit on total monthly sales only.
* Excel export and safety-stock recommendations are not implemented in the current script.
