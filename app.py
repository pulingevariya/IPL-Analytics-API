# Import necessary modules from Flask and API.
from flask import Flask, request
import api

# Initialize Flask application.
app = Flask(__name__)

# Define an endpoint to get teams for a particular season.
@app.route('/api/teamsperseason')
def teamsPerSeason():
    season = request.args.get('season')  # Extract 'season' parameter from the request.
    response = api.teamsPerSeason(season)
    return response

# Define an endpoint to get teams based on a team name.
@app.route('/api/teamsperteam')
def teamsPerTeam():
    team = request.args.get('team')  # Extract 'team' parameter from the request.
    response = api.teamsPerTeam(team)
    return response

# Define an endpoint to get teams for a particular season and team.
@app.route('/api/teamsperseasonteam')
def teamsPerSeasonTeam():
    season = request.args.get('season')
    team = request.args.get('team')
    response = api.teamsPerSeasonTeam(season, team)
    return response

# Define an endpoint to get batsmen data across all seasons.
@app.route('/api/batsmenperallseasons')
def batsmenPerAllSeasons():
    response = api.batsmenPerAllSeasons()
    return response

# Define an endpoint to get batsmen data for a specific season.
@app.route('/api/batsmenperseason')
def batsmenPerSeason():
    season = request.args.get('season')
    response = api.batsmenPerSeason(season)
    return response

# Define an endpoint to get bowlers data across all seasons.
@app.route('/api/bowlersperallseasons')
def bowlersPerAllSeasons():
    response = api.bowlersPerAllSeasons()
    return response

# Define an endpoint to get bowlers data for a specific season.
@app.route('/api/bowlersperseason')
def bowlersPerSeason():
    season = request.args.get('season')
    response = api.bowlersPerSeason(season)
    return response

# Define an endpoint to get season-wise data across all seasons.
@app.route('/api/allseasons')
def allSeasons():
    teams_dict = api.overallAllSeasonsAPI()
    return teams_dict

# Define an endpoint to get data for a particular season.
@app.route('/api/season')
def season():
    season = request.args.get('season')
    response = api.overallSeasonAPI(season)
    return response

# Define an endpoint to get data for a specific team across all seasons.
@app.route('/api/teamallseasons')
def teamallseasons():
    team = request.args.get('team')
    response = api.teamAllSeasonsAPI(team)
    return response

# Define an endpoint to get data for a specific team in a specific season.
@app.route('/api/teamseason')
def teamseason():
    team = request.args.get('team')
    season = request.args.get('season')
    response = api.teamSeasonAPI(team, season)
    return response

# Define an endpoint to get team vs team data across all seasons.
@app.route('/api/teamvsteamallseasons')
def teamVsTeamAllSeasons():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    response = api.teamVsTeamAllSeasonsAPI(team1, team2)
    return response

# Define an endpoint to get team vs team data for a specific season.
@app.route('/api/teamvsteamseason')
def teamVsTeamSeason():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    season = request.args.get('season')
    response = api.teamVsTeamSeasonAPI(team1, team2, season)
    return response

# Define an endpoint to get batsman's data across all seasons.
@app.route('/api/batsmanallseasons')
def batsmanAllSeasons():
    batsman = request.args.get('batsman')
    response = api.batsmanAllSeasonsAPI(batsman)
    return response

# Define an endpoint to get batsman's data for a specific season.
@app.route('/api/batsmanseason')
def batsmanSeason():
    batsman = request.args.get('batsman')
    season = request.args.get('season')
    response = api.batsmanSeasonAPI(batsman, season)
    return response

# Define an endpoint to get bowler's data across all seasons.
@app.route('/api/bowlerallseasons')
def bowlerAllSeasons():
    bowler = request.args.get('bowler')
    response = api.bowlerAllSeasonsAPI(bowler)
    return response

# Define an endpoint to get bowler's data for a specific season.
@app.route('/api/bowlerseason')
def bowlerSeason():
    bowler = request.args.get('bowler')
    season = request.args.get('season')
    response = api.bowlerSeasonAPI(bowler, season)
    return response

# Run the Flask application if this script is the main program.
if __name__ == '__main__':
    app.run(debug=True)
