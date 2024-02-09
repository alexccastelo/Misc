from flask import Flask, render_template, request, jsonify
import requests
from babel import Locale
from babel.dates import format_date, format_datetime, format_time
from babel.numbers import format_currency
import pytz
from datetime import datetime

locale = "pt_BR"
# Configura o fuso horário para UTC-3 para o horário de Brasília
fuso_horario = pytz.timezone("America/Sao_Paulo")
# Configura o formato de data e hora
data_hora_atual = datetime.now(fuso_horario).strftime("%d-%m-%Y / %H:%M:%S")


app = Flask(__name__)

BASE_URL = "https://economia.awesomeapi.com.br/last/"


@app.route("/", methods=["GET", "POST"])
def index():
    moedas = [
        "USD-BRL",
        "EUR-BRL",
        "BTC-BRL",
        "CNY-BRL",
        "ARS-BRL",
    ]  # Atualize esta lista com as moedas do seu arquivo XML
    if request.method == "POST":
        moeda = request.form.get("moeda")
        resposta = requests.get(f"{BASE_URL}{moeda}")
        if resposta.status_code == 200:
            data = resposta.json()
            moeda_origem, moeda_destino = moeda.split("-")
            taxa = data[f"{moeda_origem}{moeda_destino}"]["bid"]
            # Formata a taxa com quatro casas decimais para o padrão de moeda
            # if "BRL" in moeda_destino:
            #    simbolo_moeda = "r$"
            # else:
            #    simbolo_moeda = ""  # Você pode expandir esta lógica para outras moedas
            taxa = float(taxa)  # Garante que a taxa seja um número real
            taxa_formatada = format_currency(taxa, "BRL", locale=locale)
            taxa_formatada = taxa_formatada.replace(".", ",").replace(",", ".", 1)

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
