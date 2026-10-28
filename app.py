from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!doctype html>
    <html lang="da">
    <head>
        <meta charset="utf-8">
        <title>Min webterminal</title>
    </head>
    <body style="background:#111;color:#0f0;font-family:monospace;padding:30px">
        <h2>Min webterminal</h2>
        <p>Serveren kører.</p>
        <p>Velkommen til min hjemmeside!</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
