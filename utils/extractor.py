import os
import re
import csv
from datetime import datetime

siglas_estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
                  'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR',
                  'SC', 'SP', 'SE', 'TO']

def arquivo_tem_sigla(arquivo):
    nome = os.path.basename(arquivo).upper()
    return any(nome.startswith(sigla) for sigla in siglas_estados)

def extrair_emails(arquivo, palavras_chave):
    emails_encontrados = set()
    try:
        with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                for palavra in palavras_chave:
                    padrao = re.compile(rf'\b[\w.%+-]*{palavra}[\w.%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{{2,4}}\b', re.IGNORECASE)
                    emails = padrao.findall(linha)
                    emails_encontrados.update(emails)
    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")
    return emails_encontrados

def processar_arquivos(lista_arquivos, palavras_chave, caminho_saida):
    todos_emails = set()
    for arquivo in lista_arquivos:
        if arquivo_tem_sigla(arquivo):
            emails = extrair_emails(arquivo, palavras_chave)
            todos_emails.update(emails)

    with open(caminho_saida, 'w', encoding='utf-8') as f_out:
        for email in sorted(todos_emails):
            f_out.write(email + '\n')
    salvar_log(os.path.basename(caminho_saida), len(todos_emails))

def salvar_log(nome_arquivo, total_emails):
    os.makedirs("logs", exist_ok=True)
    caminho_log = os.path.join("logs", "extracoes.csv")

    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(caminho_log, 'a', encoding='utf-8', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow([nome_arquivo, data_hora, total_emails])
