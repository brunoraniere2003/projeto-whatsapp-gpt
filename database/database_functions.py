from openpyxl import load_workbook, Workbook
from datetime import datetime

def adicionar_linha_excel(nome, numero, msg_usuario, msg_gpt):
    # Carregar ou criar o arquivo Excel
    caminho_arquivo = 'database/registro.xlsx'
    try:
        workbook = load_workbook(caminho_arquivo)
        sheet = workbook.active
    except FileNotFoundError:
        # Criar o arquivo e as colunas se não existir
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["nome", "numero", "msg_usuario", "msg_gpt", "hora"])

    # Adicionar os dados
    hora = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append([nome, numero, msg_usuario, msg_gpt, hora])

    # Salvar o arquivo
    workbook.save(caminho_arquivo)
    workbook.close()