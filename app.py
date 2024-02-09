from flask import Flask, request, render_template_string
import os
from pytube import YouTube

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Download de Vídeo do YouTube</title>
</head>
<body>
    <h1>Download de Vídeo do YouTube</h1>
    <form method="post">
        <label for="url">URL do Vídeo:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Baixar Vídeo</button>
    </form>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def baixar_video():
    if request.method == "POST":
        url = request.form["url"]
        caminho_destino = "videos"
        try:
            # Criar um objeto YouTube
            yt = YouTube(url)

            # Obter a melhor stream disponível (resolução mais alta)
            video_stream = yt.streams.get_highest_resolution()

            # Criar o diretório de destino se não existir
            if not os.path.exists(caminho_destino):
                os.makedirs(caminho_destino)

            # Baixar o vídeo
            video_stream.download(caminho_destino)
            return f"Download de '{yt.title}' concluído!"
        except Exception as e:
            return f"Erro ao baixar vídeo: {e}"
    return render_template_string(HTML_FORM)


if __name__ == "__main__":
    app.run(debug=True)
