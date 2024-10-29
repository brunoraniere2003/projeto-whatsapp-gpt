from openpyxl import load_workbook
import pandas as pd
import os
from datetime import datetime

def adicionar_linha_excel(nome, numero, msg_usuario, msg_gpt, hora=None):
    caminho_arquivo = os.path.join("database", "registro.xlsx")

    # Cria o arquivo se ele não existir, com cabeçalhos
    if not os.path.exists(caminho_arquivo):
        from openpyxl import Workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["nome", "numero", "msg_usuario", "msg_gpt", "hora"])  # Cabeçalhos
        workbook.save(caminho_arquivo)

    # Carrega o arquivo e insere a nova linha com 'hora'
    workbook = load_workbook(caminho_arquivo)
    sheet = workbook.active
    if hora is None:  # Caso a hora não seja passada, gera a hora atual
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([nome, numero, msg_usuario, msg_gpt, hora])
    workbook.save(caminho_arquivo)

def visualizar_registros_excel():
    caminho_arquivo = os.path.join("database", "registro.xlsx")
    
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