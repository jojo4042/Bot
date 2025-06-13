from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Configuration API
API_KEY = "TON_API_KEY_ICI"  # Mets ta vraie clé API entre guillemets
API_BASE = "https://v3.football.api-sports.io"
LEAGUE_ID = 61  # Ligue 1 France
SEASON = 2023

HEADERS = {
    "x-apisports-key": API_KEY
}

# Récupération des matchs à venir (mode démo ici)
def get_upcoming_matches(league_id=LEAGUE_ID, season=SEASON, next_n=10):
    print("⚠️ Mode démo activé : données statiques utilisées (pas d'appel API)")
    return [
        {
            'fixture_id': 123,
            'date': '2025-06-15',
            'time': '21:00',
            'home_team': 'Paris SG',
            'home_id': 85,
            'away_team': 'Marseille',
            'away_id': 81,
            'league': 'Ligue 1',
            'venue': 'Parc des Princes'
        },
        {
            'fixture_id': 456,
            'date': '2025-06-16',
            'time': '18:30',
            'home_team': 'Lyon',
            'home_id': 79,
            'away_team': 'Monaco',
            'away_id': 83,
            'league': 'Ligue 1',
            'venue': 'Groupama Stadium'
        }
    ]

# Route principale
@app.route("/", methods=["GET"])
def index():
    matches = get_upcoming_matches()
    return render_template("index.html", matches=matches, prediction=None)

# Route de prédiction
@app.route("/predict", methods=["POST"])
def predict():
    home_id = request.form.get("home_id")
    away_id = request.form.get("away_id")

    print(f"🔮 Prédiction demandée : Home ID = {home_id}, Away ID = {away_id}")

    # ➕ Exemple de prédiction bidon (à remplacer plus tard par une vraie logique)
    if int(home_id) > int(away_id):
        prediction = f"Victoire probable de l’équipe à domicile (ID {home_id})"
    else:
        prediction = f"Victoire probable de l’équipe à l’extérieur (ID {away_id})"

    matches = get_upcoming_matches()
    return render_template("index.html", matches=matches, prediction=prediction)

# Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
