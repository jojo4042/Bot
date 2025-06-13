from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Erreur lors du rendu : {e}"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        team1_id = request.form.get('team1')
        team2_id = request.form.get('team2')

        if not team1_id or not team2_id:
            return render_template("index.html", error="Veuillez sélectionner les deux équipes.")

        # Exemple simple : simulation prédiction
        prediction = "Équipe 1 favorite" if team1_id > team2_id else "Équipe 2 favorite"

        return render_template("index.html", prediction=prediction)

    except Exception as e:
        return render_template("index.html", error=f"Erreur serveur : {e}")


        headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': 'YOUR_API_KEY'
        }

        def get_form_score(team_id):
            url = f"https://v3.football.api-sports.io/teams/statistics?league=61&season=2023&team={team_id}"
            response = requests.get(url, headers=headers)
            data = response.json()
            form = data.get("response", {}).get("form", "")
            return form.count("W")

        team1_score = get_form_score(team1_id)
        team2_score = get_form_score(team2_id)

        if team1_score > team2_score:
            prediction = "Équipe 1"
        elif team2_score > team1_score:
            prediction = "Équipe 2"
        else:
            prediction = "Égalité"

        return render_template("index.html", prediction=prediction, team1_score=team1_score, team2_score=team2_score)
    else:
        return render_template("index.html")
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

