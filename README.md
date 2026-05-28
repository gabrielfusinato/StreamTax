# IRPF Analytics - Age-Based Tax Dashboard

An interactive dashboard that analyzes **Brazilian Income Tax (IRPF)** refund data broken down by **age group**, built with **Python**, **Streamlit**, **Supabase**, and **Plotly**.
This project was developed to practice **database integration (PostgreSQL)**, **messy real-world data cleaning**, and **interactive data visualization**.

---

## 🛠️ Setup

Install the necessary dependencies to connect to the database and run the dashboard:

```bash
pip install streamlit supabase pandas plotly python-dotenv
```

Create a `.env` file in the project root with your Supabase credentials:

```env
SUPABASE_URL=your-project-url
SUPABASE_PUBLISHABLE_KEY=your-anon-key
```

## 🚀 Execution

To start the application, run:

```bash
streamlit run streamlit_ui.py
```

---

## 🧠 Project Logic & Study Goals

The core of this project is turning raw, inconsistently formatted tax data into a clean, trustworthy dashboard. The logic covers:

* **Cloud Integration:** Using the `supabase-py` client to fetch records from a PostgreSQL table hosted on Supabase.
* **Brazilian Number Parsing:** Raw values are stored as text in Brazilian format (`.` as thousands separator, `,` as decimal, `-` for missing data). The backend normalizes them into proper numeric types before any analysis.
* **Handling Overlapping Age Brackets:** The source data reports `≥ 60` and `≥ 80` as **nested** ranges — the 80+ group is *contained inside* the 60+ group. Summing them naively would **double-count** older taxpayers. The app de-nests them into mutually exclusive brackets (`60–79 = acima_60 − acima_80`) so totals are correct.
* **Robust Visualization:** Missing values are coerced to zero, age groups are ordered explicitly, and the financial dimension is shown across separate, easy-to-read Plotly charts instead of a fragile dual-axis plot.
* **Performance:** Streamlit caching (`@st.cache_resource` for the client, `@st.cache_data` for the dataset) avoids re-querying the database on every interaction.

---

## 📊 Features

* Month selector to inspect any reporting period.
* Headline metrics: **total taxpayers** and **total amount (R$)**, free of double-counting.
* Contributors per age group.
* Average amount per person per age group.
* Total amount collected per age group.

---

## 💾 Database Setup (SQL)

Run this command in your **Supabase SQL Editor** to initialize the table.
Columns are stored as `text` on purpose — the raw data carries Brazilian formatting that is cleaned in Python at load time:

```sql
CREATE TABLE irpf_bruto (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mounth          TEXT,
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

---

## 🗂️ Project Structure

```
.
├── main.py          # Backend: Supabase client + data fetching/cleaning
├── streamlit_ui.py  # Frontend: dashboard and Plotly charts
├── .env             # Credentials (not committed)
└── README.md
```

---
> **Developed for study purposes:** Python Integration + Data Cleaning + Database Management + Data Visualization.