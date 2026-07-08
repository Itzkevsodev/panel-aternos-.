from flask import Flask, render_template_string
from python_aternos import Client
import os

app = Flask(__name__)

# Récupération sécurisée des identifiants (configurés sur Render)
ATERNOS_USER = os.environ.get("ATER_USER")
ATERNOS_PASS = os.environ.get("ATER_PASS")

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mon Panel Serveur</title>
    <style>
        body { background: #0a0a0a; color: #00ff66; font-family: 'Courier New', monospace; text-align: center; padding-top: 100px; }
        .box { border: 2px solid #00ff66; display: inline-block; padding: 30px; border-radius: 10px; background: #111; box-shadow: 0 0 15px #00ff66; }
        .btn { background: #00ff66; color: black; padding: 15px 40px; font-size: 20px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; margin-top: 20px; }
        .btn:hover { background: #00cc55; box-shadow: 0 0 10px #00ff66; }
    </style>
</head>
<body>
    <div class="box">
        <h1>⚡ LANCEUR DE SERVEUR FFA ⚡</h1>
        <p>[ Statut : Prêt à être synchronisé ]</p>
        <form action="/demarrer" method="post">
            <button type="submit" class="btn">🚀 ALLUMER LE SERVEUR</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/demarrer', methods=['POST'])
def start_server():
    if not ATERNOS_USER or not ATERNOS_PASS:
        return "<h1>❌ Erreur : Identifiants Aternos manquants sur Render !</h1>"
    
    try:
        atclient = Client.from_credentials(ATERNOS_USER, ATERNOS_PASS)
        servs = atclient.list_servers()
        
        # Lance le premier serveur du compte
        mon_serveur = servs[0]
        mon_serveur.start()
        return "<h1>🔥 Ordre reçu ! Ton serveur Aternos démarre, check ton Minecraft d'ici 2 min !</h1>"
    except Exception as e:
        return f"<h1>❌ Erreur Aternos : {e} (Vérifie tes identifiants)</h1>"

if __name__ == '__main__':
    # Render utilise la variable PORT, sinon on met 8080 par défaut
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
