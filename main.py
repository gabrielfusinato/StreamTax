import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def start_supabase():
    supabase: Client = create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_PUBLISHABLE_KEY")      
    )
    return supabase

def fetch_irpf_data(supabase: Client) -> pd.DataFrame:
    response = supabase.table("irpf_bruto").select("*").execute()
    df = pd.DataFrame(response.data)
    
    if not df.empty:
        for col in df.columns:
            if col not in ['id', 'mounth', 'created_at']:
                limpo = df[col].astype(str).str.strip()
                limpo = limpo.replace('None', '').replace('nan', '')
                limpo = limpo.str.replace('.', '', regex=False).str.replace(',', '.')
                df[col] = pd.to_numeric(limpo, errors='coerce')
                
    return df