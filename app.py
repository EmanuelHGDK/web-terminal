
import os
from threading import Lock
from flask import Flask, request
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = set()
clients_lock = Lock()

PAGE = """
<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Webterminal Chat</title>
<style>
body {
  background:#111;color:#00ff66;
  font-family:monospace;padding:20px;
}
#log {
  height:60vh;overflow:auto;border:1px solid #00ff66;
  padding:12px;white-space:pre-wrap;overflow-wrap:anywhere;
}
input,button {
  background:#111;color:#00ff66;border:1px solid #00ff66;
  padding:10px;font-family:monospace;
}
input { box-sizing:border-box;width:75%; }
</style>
</head>
<body>
<h2>Webterminal Chat</h2>
<p id="status">Forbinder...</p>
<div id="log"></div>
<form id="form">
  <input id="message" autocomplete="off" placeholder="Skriv en besked...">
  <button type="submit">Send</button>
</form>
<script>
const log = document.getElementById("log");
const status = document.getElementById("status");
const form = document.getElementById("form");
const input = document.getElementById("message");

function addLine(text) {
  const line = document.createElement("div");
  line.textContent = text;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

const token = prompt("Indtast CHAT_TOKEN fra Render:");
if (token) {
  const scheme = location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(
    scheme + "//" + location.host + "/ws?token=" +
    encodeURIComponent(token)
  );

  ws.onopen = () => status.textContent = "Forbundet";
  ws.onclose = () => status.textContent = "Afbrudt";
  ws.onerror = () => status.textContent = "Forbindelsesfejl";
  ws.onmessage = event => addLine(event.data);

  form.addEventListener("submit", event => {
    event.preventDefault();
    const text = input.value.trim();
    if (text && ws.readyState === WebSocket.OPEN) {
      ws.send(text);
      input.value = "";
    }
  });
} else {
  status.textContent = "Token mangler";
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return PAGE

@sock.route("/ws")
def chat(ws):
    expected = os.environ.get("CHAT_TOKEN", "")
    supplied = request.args.get("token", "")

    if not expected or supplied != expected:
        ws.close()
        return

    with clients_lock:
        clients.add(ws)

    try:
        ws.send("Forbundet til chatserveren.")
        while True:
            message = ws.receive()
            if message is None:
                break

            # Send kun almindelige tekstbeskeder videre.
            if len(message) > 2000:
                ws.send("Beskeden er for lang (maks. 2000 tegn).")
                continue

            with clients_lock:
                recipients = list(clients)

            for client in recipients:
                try:
                    client.send("Klient: " + message)
                except Exception:
                    with clients_lock:
                        clients.discard(client)
    finally:
        with clients_lock:
            clients.discard(ws)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000"))
    )
