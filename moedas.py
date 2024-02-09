from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import pytz
import locale


locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

app = Flask(__name__)

BASE_URL = "https://economia.awesomeapi.com.br/last/"


@app.route("/", methods=["GET", "POST"])
def index():
    moedas = [
        "USD-BRL",
        "EUR-BRL",
        "BTC-BRL",
    ]  # Atualize esta lista com as moedas do seu arquivo XML
    if request.method == "POST":
        moeda = request.form.get("moeda")
        resposta = requests.get(f"{BASE_URL}{moeda}")
        if resposta.status_code == 200:
            data = resposta.json()
            moeda_origem, moeda_destino = moeda.split("-")
            taxa = data[f"{moeda_origem}{moeda_destino}"]["bid"]
            # Formata a taxa com quatro casas decimais para o padrão de moeda
            if "BRL" in moeda_destino:
                simbolo_moeda = "R$"
            else:
                simbolo_moeda = ""  # Você pode expandir esta lógica para outras moedas
            taxa = float(taxa)  # Garante que a taxa seja um número real
            taxa_formatada = locale.format_string("%.4f", taxa, grouping=True)
            taxa_formatada = simbolo_moeda + taxa_formatada.replace(".", ",").replace(
                ",", ".", 1
            )
            # Configura o fuso horário para UTC-3
            fuso_horario = pytz.timezone("America/Sao_Paulo")
            data_hora_atual = datetime.now(fuso_horario).strftime("%d-%m-%Y / %H:%M:%S")
            return render_template(
                "index.html",
                moedas=moedas,
                taxa=taxa_formatada,
                data_hora_atual=data_hora_atual,
                moeda=moeda,
                atualizacao=True,
            )
        else:
            return "Erro na API de cotações", 500
    return render_template("index.html", moedas=moedas)


if __name__ == "__main__":
    app.run(debug=True)
