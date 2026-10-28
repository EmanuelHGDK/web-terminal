
import os
import socket
from flask import Flask

app = Flask(__name__)

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except OSError:
        return "Ukendt"

@app.route("/")
def home():
    local_ip = get_local_ip()
    port = os.environ.get("PORT", "10000")

    return f"""
    <!doctype html>
    <html lang="da">
    <head>
        <meta charset="utf-8">
        <title>Serverstatus</title>
    </head>
    <body style="background:#111;color:#00ff66;
                 font-family:monospace;padding:30px">
        <h1>Serverstatus</h1>
        <p>Serverens lokale IP: {local_ip}</p>
        <p>Appens interne port: {port}</p>
        <p>Offentlig adresse:
           <a style="color:#00ff66"
              href="https://web-terminal-madb.onrender.com">
              Åbn hjemmesiden
           </a>
        </p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
