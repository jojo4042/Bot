from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = 0393053d71e47ea11117cacb6cf65a99
API_URL = 'https://v3.football.api-sports.io/fixtures'

headers = {
    'x-apisports-key': API_KEY
}

def get_upcoming_matches():
    params = {
        'next': 10  # récupérer les 10 prochains matchs
    }
    response = requests.get(API_URL, headers=headers, params=params)
    data = response.json()
    matches = []
    if data.get('response'):
        for item in data['response']:
            fixture = item['fixture']
            teams = item['teams']
            league = item['league']
            matches.append({
                'date': fixture['date'],
                'time': fixture['date'][11:16],  # extraire l’heure (HH:MM)
                'home_team': teams['home']['name'],
                'away_team': teams['away']['name'],
                'league': league['name'],
                'venue': fixture.get('venue', {}).get('name', 'N/A')
            })
    return matches

@app.route('/')
def index():
    matches = get_upcoming_matches()
    return render_template('index.html', matches=matches)

if __name__ == '__main__':
    app.run(debug=True)



@app.route("/predict", methods=["POST"])
def predict():
    team1 = request.form.get("team1")
    team2 = request.form.get("team2")
    
    # ➕ result = "Prédiction à venir..."i
    result = f"Équipe 1 : {team1}, Équipe 2 : {team2}"  # juste pour tester
    
    return render_template("index.html", prediction=result)
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

