import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from main import start_supabase, fetch_irpf_data

st.set_page_config(page_title="IRPF Analytics", layout="wide")

AGE_GROUPS = [
    {"label": "≤ 18",  "qty": "qtd_ate_18", "val": "valor_ate_18"},
    {"label": "19–25", "qty": "qtd_19_25",  "val": "valor_19_25"},
    {"label": "26–30", "qty": "qtd_26_30",  "val": "valor_26_30"},
    {"label": "31–40", "qty": "qtd_31_40",  "val": "valor_31_40"},
    {"label": "41–50", "qty": "qtd_41_50",  "val": "valor_41_50"},
    {"label": "51–59", "qty": "qtd_51_59",  "val": "valor_51_59"},
    {"label": "60–79", "qty": "qtd_acima_60", "val": "valor_acima_60",
     "minus_qty": "qtd_acima_80", "minus_val": "valor_acima_80"},
    {"label": "80+",   "qty": "qtd_acima_80",  "val": "valor_acima_80"},
]

@st.cache_resource
def get_supabase_client():
    return start_supabase()

@st.cache_data
def load_data():
    client = get_supabase_client()
    return fetch_irpf_data(client)

def safe_get(row, col):
    """Pega o valor da coluna tratando ausência/NaN como 0."""
    if col is None or col not in row.index:
        return 0.0
    v = row[col]
    return 0.0 if pd.isna(v) else float(v)


def group_value(row, group, kind):
    """kind = 'qty' ou 'val'. Aplica a subtração quando a faixa é exclusiva."""
    base = safe_get(row, group[kind])
    minus_key = "minus_qty" if kind == "qty" else "minus_val"
    if minus_key in group:
        base -= safe_get(row, group[minus_key])
    return max(base, 0.0) 


def fmt_int(n):
    return f"{int(round(n)):,}".replace(",", ".")


def fmt_brl(n):
    return f"R$ {n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.title("📊 IRPF Age Analytics Dashboard")

df = load_data()

if df.empty:
    st.warning("No data found in the database.")
    st.stop()

col_mes = "mes" if "mes" in df.columns else "mes"

expected = {g[k] for g in AGE_GROUPS for k in ("qty", "val", "minus_qty", "minus_val") if k in g}
missing = sorted(expected - set(df.columns))
if missing:
    st.error(f"Colunas não encontradas na tabela (ajuste AGE_GROUPS): {missing}")
    st.stop()

st.subheader("Taxpayers Overview")

selected_mes = st.selectbox("Select a mes:", df[col_mes].unique())
mes_data = df[df[col_mes] == selected_mes].iloc[0]

labels = [g["label"] for g in AGE_GROUPS]
taxpayers = [group_value(mes_data, g, "qty") for g in AGE_GROUPS]
amounts = [group_value(mes_data, g, "val") for g in AGE_GROUPS]

total_pessoas = sum(taxpayers)
total_dinheiro = sum(amounts)

col1, col2 = st.columns(2)
col1.metric("Total de Contribuintes", fmt_int(total_pessoas))
col2.metric("Total Financeiro", fmt_brl(total_dinheiro))

st.divider()

val_per_person = [
    (amt / qtd if qtd > 0 else 0.0)
    for qtd, amt in zip(taxpayers, amounts)
]

st.markdown(f"#### Distribuição por faixa etária — {selected_mes}")

c1, c2 = st.columns(2)

fig_pessoas = go.Figure(
    go.Bar(
        x=labels, y=taxpayers, marker_color="rgb(55, 83, 109)",
        hovertemplate="%{x}<br>%{y:,.0f} pessoas<extra></extra>",
    )
)
fig_pessoas.update_layout(
    title_text="Contribuintes por faixa",
    yaxis_title="Pessoas", margin=dict(t=40, b=0, l=0, r=0),
)
c1.plotly_chart(fig_pessoas, use_container_width=True)

fig_vpp = go.Figure(
    go.Bar(
        x=labels, y=val_per_person, marker_color="rgb(26, 118, 255)",
        hovertemplate="%{x}<br>R$ %{y:,.2f} por pessoa<extra></extra>",
    )
)
fig_vpp.update_layout(
    title_text="Valor médio por pessoa (R$)",
    yaxis_title="R$ / pessoa", margin=dict(t=40, b=0, l=0, r=0),
)
c2.plotly_chart(fig_vpp, use_container_width=True)

fig_total = go.Figure(
    go.Bar(
        x=labels, y=amounts, marker_color="rgb(0, 153, 102)",
        hovertemplate="%{x}<br>R$ %{y:,.2f}<extra></extra>",
    )
)
fig_total.update_layout(
    title_text="Valor total arrecadado por faixa (R$)",
    yaxis_title="R$", margin=dict(t=40, b=0, l=0, r=0),
)
st.plotly_chart(fig_total, use_container_width=True)

st.caption(
    "As faixas são mutuamente exclusivas: '60–79' = (60 ou mais) − (80 ou mais). "
    "Por isso os totais não contam o grupo 80+ duas vezes."
)