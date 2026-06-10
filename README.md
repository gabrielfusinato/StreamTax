# IRPF Analytics - Income Tax Refund by Age Dashboard

An interactive dashboard for analyzing **Brazilian Income Tax Refund (IRPF restitution)** data by **age group**, built with **Python**, **Pandas**, **Streamlit**, **Supabase**, and **Plotly**.

---

## 🛠️ Setup

Install the required dependencies:

```bash
pip install streamlit supabase pandas plotly python-dotenv
````

Create a `.env` file in the project root with your Supabase credentials:

```env
SUPABASE_URL=your-project-url
SUPABASE_PUBLISHABLE_KEY=your-anon-key
```

---

## 🗄️ Database Setup

Create the table below in the **Supabase SQL Editor**:

```sql
CREATE TABLE irpf_bruto (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mes             TEXT,
  qtd_ate_18      TEXT,  valor_ate_18    TEXT,
  qtd_19_25       TEXT,  valor_19_25     TEXT,
  qtd_26_30       TEXT,  valor_26_30     TEXT,
  qtd_31_40       TEXT,  valor_31_40     TEXT,
  qtd_41_50       TEXT,  valor_41_50     TEXT,
  qtd_51_59       TEXT,  valor_51_59     TEXT,
  qtd_acima_60    TEXT,  valor_acima_60  TEXT,
  qtd_acima_80    TEXT,  valor_acima_80  TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

The columns are stored as `TEXT` because the original dataset uses Brazilian number formatting. The data is cleaned and converted in Python before analysis.

---

## 📥 Data Ingestion

The `data_ingest.py` file reads the CSV file, renames the columns, clears the current records in the table, and inserts the new data into Supabase.

Run:

```bash
python data_ingest.py
```

---

## 🚀 Execution

To start the dashboard, run:

```bash
streamlit run streamlit_ui.py
```

---

## 🧠 Project Logic

The project is divided into three main parts:

* `data_ingest.py`: reads the CSV file and sends the raw income tax refund data to Supabase.
* `main.py`: connects to Supabase, fetches the data, cleans Brazilian number formats, and converts values to numeric types.
* `streamlit_ui.py`: builds the dashboard interface and charts.

The app analyzes **income tax refund data by age group**, showing both the number of taxpayers and the refunded amount for each group.

The app also handles overlapping age groups. In the original data, the `80+` group is included inside the `60+` group. To avoid double-counting, the dashboard creates an exclusive group:

```txt
60–79 = 60+ - 80+
```

This keeps the totals correct.

---

## 📊 Features

* Month selector.
* Total taxpayers metric.
* Total refunded amount metric.
* Taxpayers by age group chart.
* Average refund amount per person chart.
* Total refund amount by age group chart.
* Brazilian number and currency formatting.
* Streamlit cache for better performance.

---

## 🗂️ Project Structure

```txt
.
├── data_irpf.csv       # Raw income tax refund dataset
├── data_ingest.py      # CSV ingestion into Supabase
├── main.py             # Supabase connection and data cleaning
├── streamlit_ui.py     # Streamlit dashboard
├── .env                # Environment variables
└── README.md
```

---

## 📚 Data Source

This project uses open government data about **Brazilian Income Tax Refund by age group**.

```
The project was created for study purposes, focusing on data cleaning, database integration, and interactive data visualization.
```