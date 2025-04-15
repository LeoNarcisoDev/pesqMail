from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from datetime import datetime
from utils.extractor import processar_arquivos
import csv

app = Flask(__name__)
app.secret_key = 'supersegredo'  # Necessário para usar flash messages

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'resultados'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem = None

    if request.method == 'POST':
        arquivos = request.files.getlist('arquivos')
        extensoes_raw = request.form.get('extensoes')

        if not arquivos or not extensoes_raw:
            flash("⚠ Por favor, envie os arquivos e informe as palavras-chave.", "danger")
            return redirect(url_for('index'))

        extensoes = [ext.strip() for ext in extensoes_raw.split(',') if ext.strip()]

        caminhos_arquivos = []
        for arquivo in arquivos:
            if arquivo.filename.endswith('.txt'):
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
                arquivo.save(caminho)
                caminhos_arquivos.append(caminho)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_saida = f'emails_{timestamp}.txt'
        caminho_saida = os.path.join(app.config['RESULTS_FOLDER'], nome_saida)

        processar_arquivos(caminhos_arquivos, extensoes, caminho_saida)

        flash(f"✅ Extração concluída! Arquivo gerado: {nome_saida}", "success")
        return redirect(url_for('index'))

        historico = ler_historico()
        return render_template('index.html', arquivos_resultado=arquivos_resultado, historico=historico)

    def ler_historico():
        caminho_log = os.path.join("logs", "extracoes.csv")
        historico = []

        if os.path.exists(caminho_log):
            with open(caminho_log, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:
                        historico.append({
                            'arquivo': row[0],
                            'data': row[1],
                            'total': row[2]
                        })

        return sorted(historico, key=lambda x: x['data'], reverse=True)

    # Lista os arquivos já extraídos
    arquivos_resultado = sorted(os.listdir(app.config['RESULTS_FOLDER']), reverse=True)
    return render_template('index.html', arquivos_resultado=arquivos_resultado)

@app.route('/download/<nome_arquivo>')
def download(nome_arquivo):
    caminho = os.path.join(app.config['RESULTS_FOLDER'], nome_arquivo)
    if os.path.exists(caminho):
        return send_file(caminho, as_attachment=True)
    else:
        flash("Arquivo não encontrado.", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)

