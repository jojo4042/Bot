from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "0393053d71e47ea11117cacb6cf65a99"
HEADERS = {'x-apisports-key': API_KEY}
API_BASE = 'https://v3.football.api-sports.io'

LEAGUE_ID = 39   # Exemple : Premier League (à adapter)
SEASON = 2024    # Saison en cours

def get_upcoming_matches(league_id=LEAGUE_ID, season=SEASON, next_n=10):
    url = f'{API_BASE}/fixtures'
    params = {
        'league': league_id,
        'season': season,
        'next': next_n
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    data = resp.json()
    matches = []
    if data.get('response'):
        for item in data['response']:
            f = item['fixture']
            t = item['teams']
            l = item['league']
            matches.append({
                'fixture_id': f['id'],
                'date': f['date'][:10],
                'time': f['date'][11:16],
                'home_team': t['home']['name'],
                'home_id': t['home']['id'],
                'away_team': t['away']['name'],
                'away_id': t['away']['id'],
                'league': l['name'],
                'venue': f.get('venue', {}).get('name', 'N/A')
            })
    return matches

def get_team_ranking(team_id, league_id=LEAGUE_ID, season=SEASON):
    url = f'{API_BASE}/standings'
    params = {'league': league_id, 'season': season}
    resp = requests.get(url, headers=HEADERS, params=params)
    data = resp.json()
    if data.get('response'):
        for standing in data['response']:
            for team in standing['league']['standings'][0]:
                if team['team']['id'] == team_id:
                    return team['rank']
    return None

def get_last_results(team_id, league_id=LEAGUE_ID, season=SEASON, last_n=5):
    url = f'{API_BASE}/fixtures'
    params = {
        'team': team_id,
        'league': league_id,
        'season': season,
        'last': last_n
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    data = resp.json()
    results = []
    if data.get('response'):
        for fixture in data['response']:
            goals_for = None
            goals_against = None
            # Trouver si l'équipe est domicile ou extérieur
            home_id = fixture['teams']['home']['id']
            away_id = fixture['teams']['away']['id']
            score_home = fixture['goals']['home']
            score_away = fixture['goals']['away']

            if team_id == home_id:
                goals_for = score_home
                goals_against = score_away
            elif team_id == away_id:
                goals_for = score_away
                goals_against = score_home

            if goals_for is not None and goals_against is not None:
                if goals_for > goals_against:
                    results.append('W')
                elif goals_for < goals_against:
                    results.append('L')
                else:
                    results.append('D')
    return results

def calculate_form_score(results):
    if not results:
        return 0.5  # neutre si pas de données
    score = 0
    for r in results:
        if r == 'W':
            score += 3
        elif r == 'D':
            score += 1
    return score / (len(results)*3)

def predict_winner(team1_id, team2_id):
    rank1 = get_team_ranking(team1_id)
    rank2 = get_team_ranking(team2_id)

    form1 = calculate_form_score(get_last_results(team1_id))
    form2 = calculate_form_score(get_last_results(team2_id))

    if not rank1 or not rank2:
        return "Pas assez de données pour prédire"

    rank_score1 = 1 / rank1
    rank_score2 = 1 / rank2

    score1 = 0.6 * rank_score1 + 0.4 * form1
    score2 = 0.6 * rank_score2 + 0.4 * form2

    if score1 > score2:
        return "Prédiction : l'équipe à domicile a plus de chances de gagner"
    elif score2 > score1:
        return "Prédiction : l'équipe à l'extérieur a plus de chances de gagner"
    else:
        return "Prédiction : match nul probable"

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = get_upcoming_matches()

    prediction = None
    if request.method == 'POST':
        home_id = int(request.form['home_id'])
        away_id = int(request.form['away_id'])
        prediction = predict_winner(home_id, away_id)

    return render_template('index.html', matches=matches, prediction=prediction)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

