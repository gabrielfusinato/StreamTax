import os
from supabase import create_client, Client
from dotenv import load_dotenv

from rich.console import Console
from rich.table import Table

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)


def choose_data():
    menu = """
        ======================================================
                    MENU DE CONSULTA IRPF              
        ======================================================
        [1] Date                            [x] Sair 

        --- Quantidade ---                  --- Valores (R$) ---
        [2]  Até 18 anos                    [3]  Valor até 18
        [4]  19 - 25 anos                   [5]  Valor 19 - 25
        [6]  26 - 30 anos                   [7]  Valor 26 - 30
        [8]  31 - 40 anos                   [9]  Valor 31 - 40
        [10] 41 - 50 anos                   [11] Valor 41 - 50
        [12] 51 - 59 anos                   [13] Valor 51 - 59
        [14] 60+ anos                       [15] Valor 60+
        [16] 80+ anos                       [17] Valor 80+
        ======================================================
        Escolha uma opção: """
    
    answer = str(input(menu).strip())[0:]

    return answer

def analyse_data():

    while True:
        answer = choose_data()

        if answer.upper() == 'X':
            print("Exiting...")
            break

        match answer:
            case "1":
                column_name = "mounth" 
            case "2":
                column_name = "qtd_ate_18" 
            case "3":
                column_name = "valor_ate_18"
            case "4":
                column_name = "qtd_19_25"
            case "5":
                column_name = "valor_19_25"
            case "6":
                column_name = "qtd_26_30"
            case "7":
                column_name = "valor_26_30"
            case "8":
                column_name = "qtd_31_40"
            case "9":
                column_name = "valor_31_40"
            case "10":
                column_name = "qtd_41_50"
            case "11":
                column_name = "valor_41_50"
            case "12":
                column_name = "qtd_51_59"
            case "13":
                column_name = "valor_51_59"
            case "14":
                column_name = "qtd_acima_60"
            case "15":
                column_name = "valor_acima_60"
            case "16":
                column_name = "qtd_acima_80"
            case "17":
                column_name = "valor_acima_80"
            case _:
                print("Opção inválida.\n")
                continue
            
        try: 
            #data = read_data(column_name)
            #print(data)

            data = read_data(column_name)
            display_table(column_name, data)
            
        except ValueError:
            print("Please type a valid number or 'X'.")

        except Exception as e:
            print(f"We found no data about that. Problem detected:\n{e}")

        input("\nPRESS ANY KEY TO CONTINUE")


def read_data(coluna):
    """response = supabase.table("irpf_bruto").select(coluna).execute()
    valores = [linha[coluna] for linha in response.data]"""
    response = supabase.table("irpf_bruto").select(f"mounth, {coluna}").execute()

    #return valores
    return response.data


#só pra sair bonito
def display_table(coluna_escolhida, dados):
    console = Console()
    tabela = Table(title=f"Dados por Mês: {coluna_escolhida}")
    
    tabela.add_column("Mês", style="magenta", justify="center")
    tabela.add_column(coluna_escolhida, style="cyan", justify="center")

    for item in dados:
        tabela.add_row(str(item['mounth']), str(item[coluna_escolhida]))

    console.print(tabela)


def main():
    print("Welcome to Brazil's public data consulting!")
    analyse_data()


if __name__ == "__main__":
    main()