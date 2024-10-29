from openpyxl import load_workbook
import pandas as pd
import os

def adicionar_linha_excel(nome, numero, msg_usuario, msg_gpt):
    caminho_arquivo = os.path.join("database", "registro.xlsx")

    if not os.path.exists(caminho_arquivo):
        from openpyxl import Workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["nome", "numero", "msg_usuario", "msg_gpt", "hora"])  # Cabeçalhos
        workbook.save(caminho_arquivo)

    workbook = load_workbook(caminho_arquivo)
    sheet = workbook.active
    sheet.append([nome, numero, msg_usuario, msg_gpt])
    workbook.save(caminho_arquivo)

def visualizar_registros_excel():
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "registro.xlsx")    
    
    try:
        # Lê o arquivo Excel usando pandas
        df = pd.read_excel(caminho_arquivo)
        
        # Converte o DataFrame para uma lista de dicionários
        registros = df.to_dict(orient="records")
        
        return registros

    except FileNotFoundError:
        return {"error": "Arquivo não encontrado"}
    except Exception as e:
        return {"error": str(e)}