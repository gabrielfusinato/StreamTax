```markdown
# StreamTax

A simple and efficient tool for querying and analyzing IRPF (Brazilian Individual Income Tax) refund batch data divided by age group. The project establishes communication between a **Python** backend, a **Supabase** cloud database (PostgreSQL), and a rich terminal visual interface using **Rich**. 

The scope foresees the evolution to an interactive web interface using **Streamlit** and the automation of the data pipeline for daily updates.

---

## 🛠️ Setup

Install the necessary dependencies to connect to the database and manage the terminal interface:

```bash
pip install supabase python-dotenv rich

```

## 🚀 Execution

To start the application and access the interactive query menu via terminal, run:

```bash
python main.py

```

---

## 🧠 Project Logic & Study Goals

The core of this project is based on structuring public data and the dynamic consumption of information stored in the cloud. The developed logic covers:

* **Database Schema:** Structuring a relational table in PostgreSQL capable of segregating quantitative data (taxpayer count) and financial data (values in BRL) by age groups.
* **Query Mapping:** Implementation of a control structure (`match/case`) that translates menu interactions into specific column calls in the database.
* **Read Operations:** Integration with the `supabase-py` client to fetch data dynamically based on user choices.
* **Advanced Console Interface:** Using the `Rich` library for formatting and building stylized tables directly in the terminal.
* **Planning for Future Features:**
* Building visual dashboards and interactive charts with **Streamlit**.
* Developing data automation routines for daily verification and automatic ingestion of new updates.



---

## 💾 Database Setup (SQL)

Run this command in your **Supabase SQL Editor** to initialize the table with the exact fields corresponding to the system logic:

```sql
CREATE TABLE irpf_bruto (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mounth TEXT,
  qtd_ate_18 TEXT,
  valor_ate_18 TEXT,
  qtd_19_25 TEXT,
  valor_19_25 TEXT,
  qtd_26_30 TEXT,
  valor_26_30 TEXT,
  qtd_31_40 TEXT,
  valor_31_40 TEXT,
  qtd_41_50 TEXT,
  valor_41_50 TEXT,
  qtd_51_59 TEXT,
  valor_51_59 TEXT,
  qtd_acima_60 TEXT,
  valor_acima_60 TEXT,
  qtd_acima_80 TEXT,
  valor_acima_80 TEXT
);

```

---

> **Developed for study purposes:** Python Integration + Database Management + Public Data Analysis.

```

```