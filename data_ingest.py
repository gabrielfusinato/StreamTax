import pandas as pd
from main import start_supabase

supabase = start_supabase()

url = "https://www.gov.br/receitafederal/dados/lote-irpf-idade.csv/@@download/file/lotes_irpf_idade.csv"

df = pd.read_csv(url, sep=";")

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Mês": "mes",
    "Até 18 anos": "qtd_ate_18",
    "R$ até 18 anos": "valor_ate_18",
    "19-25 anos": "qtd_19_25",
    "R$ 19-25 anos": "valor_19_25",
    "26-30 anos": "qtd_26_30",
    "R$ 26-30 anos": "valor_26_30",
    "31-40 anos": "qtd_31_40",
    "R$ 31-40 anos": "valor_31_40",
    "41-50 anos": "qtd_41_50",
    "R$ 41-50 anos": "valor_41_50",
    "51-59 anos": "qtd_51_59",
    "R$ 51-59 anos": "valor_51_59",
    "≥ 60 anos": "qtd_acima_60",
    "R$ ≥ 60 anos": "valor_acima_60",
    "≥ 80 anos": "qtd_acima_80",
    "R$ ≥ 80 anos": "valor_acima_80",
})

data = df.to_dict(orient='records')

response = supabase.table('irpf_bruto').delete().neq("mes", " ").execute()

try:
    response = supabase.table('irpf_bruto').insert(data).execute()

except Exception as e:
    print(f"Can't isert data. Error {e}")

else: 
    print("Data inserted.")

finally:
    print("Finished.")


