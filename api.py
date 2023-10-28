# Necessary imports: numpy for numerical operations, pandas for dataframe operations, and json for JSON encoding/decoding.
import numpy as np
import pandas as pd
import json

# Loading the datasets into pandas DataFrames.
ball_with_match = pd.read_csv('datasets/ball_with_match_cleaned.csv')
matches = pd.read_csv('datasets/matches_cleaned.csv')


# Custom JSON encoder to handle NumPy-specific data types that are not serializable in default JSON encoding.
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


# Function to retrieve teams for a specific season.
def teamsPerSeason(season):
    # Filter rows corresponding to the given season.
    df = ball_with_match[ball_with_match['Season'] == int(season)].copy()

    # Extract and sort unique team names.
    teams = df['Team1'].sort_values().unique().tolist()

    # Structure the data for JSON.
    data = {
        'teamsPerSeason': {
            'teams': teams
        }
    }

    # Return data in JSON format.
    return json.dumps(data, cls=NpEncoder)


# Function to retrieve teams that a particular team has played against.
def teamsPerTeam(team):
    # Filter rows where the given team is either Team1 or Team2.
    df = ball_with_match[(ball_with_match['Team1'] == team) | (ball_with_match['Team2'] == team)]

    teams = []

    # Extract teams that are different from the given team.
    for i in sorted(df[df['BattingTeam'] != team]['BattingTeam'].sort_values().unique()):
        if i != team:
            teams.append(i)

    data = {
        'teamsPerTeam': {
            'teams': teams
        }
    }

    return json.dumps(data, cls=NpEncoder)


# Function to retrieve teams that a particular team has played against in a specific season.
def teamsPerSeasonTeam(season, team):
    # Filter rows based on the given season and team.
    df = ball_with_match[(ball_with_match['Season'] == int(season)) & (
                (ball_with_match['Team1'] == team) | (ball_with_match['Team2'] == team))]
    teams = []

    # Extract teams that are different from the given team.
    for i in sorted(df[df['BattingTeam'] != team]['BattingTeam'].sort_values().unique()):
        if i != team:
            teams.append(i)

    data = {
        'teamsPerSeasonTeam': {
            'teams': teams
        }
    }

    return json.dumps(data, cls=NpEncoder)


# Function to retrieve names of batsmen across all seasons.
def batsmenPerAllSeasons():
    # Extract and sort unique batsman names.
    batsmen_names = sorted(ball_with_match['batter'].unique())

    data = {
        'batsmenPerAllSeasons': {
            'batsmenNames': batsmen_names
        }
    }

    return json.dumps(data, cls=NpEncoder)


# Function to retrieve names of batsmen for a specific season.
def batsmenPerSeason(season):
    # Filter rows based on the given season.
    df = ball_with_match[ball_with_match['Season'] == int(season)]

    # Extract and sort unique batsman names.
    batsmen_names = sorted(df['batter'].unique())

    data = {
        'batsmenPerSeason': {
            'batsmenNames': batsmen_names
        }
    }

    return json.dumps(data, cls=NpEncoder)


# Function to retrieve names of bowlers across all seasons.
def bowlersPerAllSeasons():
    # Extract and sort unique bowler names.
    bowlers_names = sorted(ball_with_match['bowler'].unique())

    data = {
        'bowlersPerAllSeasons': {
            'bowlersNames': bowlers_names
        }
    }

    return json.dumps(data, cls=NpEncoder)


# Function to retrieve names of bowlers for a specific season.
def bowlersPerSeason(season):
    # Filter rows based on the given season.
    df = ball_with_match[ball_with_match['Season'] == int(season)]

    # Extract and sort unique bowler names.
    bowlers_names = sorted(df['bowler'].unique())

    data = {
        'bowlersPerSeason': {
            'bowlersNames': bowlers_names
        }
    }

    return json.dumps(data, cls=NpEncoder)


def overallAllSeasonsAPI():
    # Calculate the total number of unique seasons.
    total_seasons_played = ball_with_match['Season'].unique().size

    # Calculate the total number of unique teams that played.
    total_teams_played = ball_with_match['Team1'].unique().size

    # Calculate the total number of unique matches.
    total_matches_played = ball_with_match['ID'].unique().size

    # Find the batsman with the highest runs in a single match and the corresponding runs.
    highest_runs_batsman_name = ball_with_match.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_runs = ball_with_match.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    # Find the bowler with the highest wickets in a single match and the corresponding wickets.
    highest_wickets_bowler_name = ball_with_match.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_wickets = ball_with_match.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    # Filter out matches with 'NoResults', those decided by the 'D/L' method, and innings other than 1st and 2nd.
    min_max_df = ball_with_match[(ball_with_match['WonBy'] != 'NoResults') & (ball_with_match['method'] != 'D/L') & (ball_with_match['innings'].isin([1, 2]))]

    # Calculate the total runs scored by each team in each innings of every match.
    temp_df = min_max_df.groupby(['ID', 'innings', 'BattingTeam'])['total_run'].sum().reset_index()

    # Find the team with the highest and lowest score in a single match and the corresponding scores.
    highest_team_score_name = temp_df.sort_values('total_run', ascending=False).iloc[0]['BattingTeam']
    highest_team_score = temp_df.sort_values('total_run', ascending=False).iloc[0]['total_run']

    lowest_team_score_name = temp_df.sort_values('total_run').iloc[0]['BattingTeam']
    lowest_team_score = temp_df.sort_values('total_run').iloc[0]['total_run']

    # Get a list of all unique teams.
    teams = sorted(set(ball_with_match['Team1'].sort_values().unique().tolist() + ball_with_match['Team2'].sort_values().unique().tolist()))

    # Get top 5 batsmen based on total runs across all matches.
    top_5_batsmen_names = ball_with_match.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_batsmen_runs = ball_with_match.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().values.tolist()

    # Get top 5 bowlers based on total wickets taken across all matches.
    top_5_bowlers_names = ball_with_match.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_bowlers_wickets = ball_with_match.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().values.tolist()

    # Get teams that won the finals and the number of times they won.
    winning_teams_names = ball_with_match[ball_with_match['MatchNumber'] == 'Final'].drop_duplicates(subset=['Season']).groupby(['WinningTeam'])['WinningTeam'].count().sort_values(ascending=False).index.tolist()
    winning_teams_titles = ball_with_match[ball_with_match['MatchNumber'] == 'Final'].drop_duplicates(subset=['Season']).groupby(['WinningTeam'])['WinningTeam'].count().sort_values(ascending=False).values.tolist()

    # Structure all the data for JSON response.
    data = {
        'overallAllSeasons' : {
            'totalSeasonsPlayed' : total_seasons_played,
            'totalTeamsPlayed' : total_teams_played,
            'totalMatchesPlayed' : total_matches_played,
            'highestRunsBatsmanName' : highest_runs_batsman_name,
            'highestRuns' : highest_runs,
            'highestWicketsBowlerName' : highest_wickets_bowler_name,
            'highestWickets' : highest_wickets,
            'highesTeamScoreName' : highest_team_score_name,
            'highesTeamScore' : highest_team_score,
            'lowestTeamScoreName' : lowest_team_score_name,
            'lowestTeamScore' : lowest_team_score,
            'teams' : {
                'names' : teams
            },
            'top5Batsmen' : {
                'names' : top_5_batsmen_names,
                'runs' : top_5_batsmen_runs
            },
            'top5Bowlers': {
                'names': top_5_bowlers_names,
                'wickets': top_5_bowlers_wickets
            },
            'winningTeams' : {
                'names' : winning_teams_names,
                'titles' : winning_teams_titles
            }
        }
    }

    # Return data in JSON format.
    return json.dumps(data, cls=NpEncoder)


def overallSeasonAPI(season):
    # Filter the dataframe for the specified season.
    df = ball_with_match[ball_with_match['Season'] == int(season)].copy()

    # Calculate the total number of unique matches played in the season.
    total_matches_played = df['ID'].unique().size

    # Calculate the total number of unique teams that played in the season.
    total_teams_played = df[df['Season'] == int(season)]['Team1'].unique().size

    # Calculate the total number of super overs played in the season.
    total_super_overs_played = df[df['SuperOver'] == 'Y']['ID'].unique().size

    # Find the batsman with the highest runs in a match for the specified season.
    highest_runs_batsman_name = df.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_runs = df.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    # Find the bowler with the highest wickets in a match for the specified season.
    highest_wickets_bowler_name = df.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_wickets = df.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    # Filter out matches with 'NoResults', those decided by the 'D/L' method, and innings other than 1st and 2nd.
    min_max_df = df[(df['WonBy'] != 'NoResults') & (df['method'] != 'D/L') & (df['innings'].isin([1, 2]))]

    # Calculate the total runs scored by each team in each innings of every match.
    temp_df = min_max_df.groupby(['ID', 'innings', 'BattingTeam'])['total_run'].sum().reset_index()

    # Find the team with the highest score in the season.
    highest_team_score_name = temp_df.sort_values('total_run', ascending=False).iloc[0]['BattingTeam']
    highest_team_score = temp_df.sort_values('total_run', ascending=False).iloc[0]['total_run']

    # Find the team with the lowest score in the season.
    lowest_team_score_name = temp_df.sort_values('total_run').iloc[0]['BattingTeam']
    lowest_team_score = temp_df.sort_values('total_run').iloc[0]['total_run']

    # Get a list of all teams that played in the most recent season.
    playing_teams = df[df['Season'] == (df['Season'].sort_values(ascending=False).head(1).values[0])]['Team1'].sort_values().unique().tolist()

    # Find the top 5 batsmen based on total runs for the season.
    top_5_batsmen_names = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_batsmen_runs = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().values.tolist()

    # Find the top 5 bowlers based on total wickets for the season.
    top_5_bowlers_names = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_bowlers_wickets = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().values.tolist()

    # Determine the winner of the final match for the season.
    winning_team_name = df[df['MatchNumber'] == 'Final']['WinningTeam'].unique()[0]

    # Structure all the data for JSON response.
    data = {
        'overallSeason' : {
            'totalMatchesPlayed' : total_matches_played,
            'totalTeamsPlayed' : total_teams_played,
            'totalSuperOverPlayed' : total_super_overs_played,
            'highestRunsBatsmanName' : highest_runs_batsman_name,
            'highestRuns' : highest_runs,
            'highestWicketsBowlerName' : highest_wickets_bowler_name,
            'highestWickets' : highest_wickets,
            'highesTeamScoreName' : highest_team_score_name,
            'highesTeamScore' : highest_team_score,
            'lowestTeamScoreName' : lowest_team_score_name,
            'lowestTeamScore' : lowest_team_score,
            'playingTeams': {
                'names': playing_teams
            },
            'top5Batsmen' : {
                'names' : top_5_batsmen_names,
                'runs' : top_5_batsmen_runs
            },
            'top5Bowlers': {
                'names': top_5_bowlers_names,
                'wickets': top_5_bowlers_wickets
            },
            'winningTeam' : winning_team_name
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def teamAllSeasonsAPI(team):
    # Filter the dataframe for matches where the specified team participated.
    df = ball_with_match[(ball_with_match['Team1'] == team) | (ball_with_match['Team2'] == team)].copy()

    # Calculate the total number of unique seasons in which the team played.
    total_seasons_played = df['Season'].unique().size

    # Calculate the total number of unique matches the team played.
    total_matches_played = df['ID'].unique().size

    # Calculate the total number of titles won by the team.
    total_titles_won = df[(df.MatchNumber == 'Final') & (df.WinningTeam == team)]['ID'].unique().size

    # Identify the batsman from the team with the highest runs in a single match and the corresponding runs.
    highest_runs_batsman_name = df[df['BattingTeam'] == team].groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_runs = df[df['BattingTeam'] == team].groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    # Identify the bowler from the opposite team with the highest wickets in a single match against the specified team and the corresponding wickets.
    highest_wickets_bowler_name = df[df['BattingTeam'] != team].groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_wickets = df[df['BattingTeam'] != team].groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    # Filter the dataframe to calculate the highest and lowest team scores.
    min_max_df = df[(df['BattingTeam'] == team) & (df['WonBy'] != 'NoResults') & (df['method'] != 'D/L') & (df['innings'].isin([1, 2]))]
    temp_df = min_max_df.groupby(['ID', 'innings', 'BattingTeam'])['total_run'].sum().reset_index()

    # Identify the highest and lowest team scores.
    highest_score_name = temp_df.sort_values('total_run', ascending=False).iloc[0]['BattingTeam']
    highest_score = temp_df.sort_values('total_run', ascending=False).iloc[0]['total_run']

    lowest_score_name = temp_df.sort_values('total_run').iloc[0]['BattingTeam']
    lowest_score = temp_df.sort_values('total_run').iloc[0]['total_run']

    # Find the top 5 batsmen from the team based on total runs.
    top_5_batsmen_names = df[df['BattingTeam'] == team].groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_batsmen_runs = df[df['BattingTeam'] == team].groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().values.tolist()

    # Find the top 5 bowlers from opposite teams based on total wickets taken against the specified team.
    top_5_bowlers_names = df[df['BattingTeam'] != team].groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_bowlers_wickets = df[df['BattingTeam'] != team].groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().values.tolist()

    # Calculate the number of matches won, drawn, and lost by the team.
    matches_won = df[df['WinningTeam'] == team]['ID'].unique().size
    matches_draw = df[df['WinningTeam'].isnull()]['ID'].unique().size
    matches_loss = total_matches_played - matches_won - matches_draw

    # Structure the data for JSON response.
    data = {
        'teamAllSeasons' : {
            'totalSeasonsPlayed' : total_seasons_played,
            'totalMatchesPlayed': total_matches_played,
            'totalTitlesWon': total_titles_won,
            'highestRunsBatsmanName': highest_runs_batsman_name,
            'highestRuns': highest_runs,
            'highestWicketsBowlerName': highest_wickets_bowler_name,
            'highestWickets': highest_wickets,
            'highesScoreName': highest_score_name,
            'highesScore': highest_score,
            'lowestScoreName': lowest_score_name,
            'lowestScore': lowest_score,
            'top5Batsmen': {
                'names': top_5_batsmen_names,
                'runs': top_5_batsmen_runs
            },
            'top5Bowlers': {
                'names': top_5_bowlers_names,
                'wickets': top_5_bowlers_wickets
            },
            'matchesWinDrawLoss' : {
                'matchesWon': matches_won,
                'matchesDraw': matches_draw,
                'matchesLoss' : matches_loss
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def teamSeasonAPI(team, season):
    # Filter the dataframe for matches where the specified team participated in the specified season.
    df = ball_with_match[((ball_with_match['Team1'] == team) | (ball_with_match['Team2'] == team)) & (ball_with_match['Season'] == int(season))].copy()

    # Calculate the total number of unique matches the team played in the specified season.
    total_matches_played = df['ID'].unique().size

    # Calculate the total number of super overs played by the team in the specified season.
    total_super_overs_played = df[df['SuperOver'] == 'Y']['ID'].unique().size

    # Calculate the number of titles won by the team in the specified season.
    titles_won = df[(df.MatchNumber == 'Final') & (df.WinningTeam == team)]['ID'].unique().size

    # Identify the batsman from the team with the highest runs in a single match of the specified season and the corresponding runs.
    highest_runs_batsman_name = df[df['BattingTeam'] == team].groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_runs = df[df['BattingTeam'] == team].groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    # Identify the bowler from the opposite team with the highest wickets in a single match against the specified team in the specified season and the corresponding wickets.
    highest_wickets_bowler_name = df[df['BattingTeam'] != team].groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_wickets = df[df['BattingTeam'] != team].groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    # Filter the dataframe to calculate the highest and lowest team scores for the specified season.
    min_max_df = df[(df['BattingTeam'] == team) & (df['WonBy'] != 'NoResults') & (df['method'] != 'D/L') & (df['innings'].isin([1, 2]))]
    temp_df = min_max_df.groupby(['ID', 'innings', 'BattingTeam'])['total_run'].sum().reset_index()

    # Identify the highest and lowest team scores for the specified season.
    highest_score_name = temp_df.sort_values('total_run', ascending=False).iloc[0]['BattingTeam']
    highest_score = temp_df.sort_values('total_run', ascending=False).iloc[0]['total_run']

    lowest_score_name = temp_df.sort_values('total_run').iloc[0]['BattingTeam']
    lowest_score = temp_df.sort_values('total_run').iloc[0]['total_run']

    # Compile a list of players from the specified team and the opposite teams for the specified season.
    players = sorted(set(df[df['BattingTeam'] == team]['batter'].unique().tolist() + df[df['BattingTeam'] != team]['bowler'].unique().tolist()))

    # Identify the top 5 batsmen from the specified team based on total runs in the specified season.
    top_5_batsmen_names = df[df['BattingTeam'] == team].groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_batsmen_runs = df[df['BattingTeam'] == team].groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().values.tolist()

    # Identify the top 5 bowlers from the opposite teams based on total wickets taken against the specified team in the specified season.
    top_5_bowlers_names = df[df['BattingTeam'] != team].groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_bowlers_wickets = df[df['BattingTeam'] != team].groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().values.tolist()

    # Calculate the number of matches won, drawn, and lost by the team in the specified season.
    matches_won = df[df['WinningTeam'] == team]['ID'].unique().size
    matches_draw = df[df['WinningTeam'].isnull()]['ID'].unique().size
    matches_loss = total_matches_played - matches_won - matches_draw

    # Structure the data for JSON response.
    data = {
        'teamSeason' : {
            'totalMatchesPlayed': total_matches_played,
            'totalSuperOverPlayed': total_super_overs_played,
            'titlesWon': titles_won,
            'highestRunsBatsmanName': highest_runs_batsman_name,
            'highestRuns': highest_runs,
            'highestWicketsBowlerName': highest_wickets_bowler_name,
            'highestWickets': highest_wickets,
            'highesScoreName': highest_score_name,
            'highesScore': highest_score,
            'lowestScoreName': lowest_score_name,
            'lowestScore': lowest_score,
            'players' : {
                'names' : players
            },
            'top5Batsmen': {
                'names': top_5_batsmen_names,
                'runs': top_5_batsmen_runs
            },
            'top5Bowlers': {
                'names': top_5_bowlers_names,
                'wickets': top_5_bowlers_wickets
            },
            'matchesWinDrawLoss' : {
                'matchesWon': matches_won,
                'matchesDraw': matches_draw,
                'matchesLoss' : matches_loss
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def teamVsTeamAllSeasonsAPI(team1, team2):
    # Filter the dataframe for matches where the specified teams played against each other.
    df = ball_with_match[((ball_with_match['Team1'] == team1) & (ball_with_match['Team2'] == team2)) | ((ball_with_match['Team1'] == team2) & (ball_with_match['Team2'] == team1))].copy()

    # Calculate the total number of unique seasons in which the teams played against each other.
    total_seasons_played = df['Season'].unique().size

    # Calculate the total number of unique matches the teams played against each other.
    total_matches_played = df['ID'].unique().size

    # Calculate the total number of super overs played by the teams against each other.
    total_super_overs_played = df[df['SuperOver'] == 'Y']['ID'].unique().size

    # Identify the batsman with the highest runs in a single match between the two teams and the corresponding runs.
    highest_runs_batsman_name = df.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_runs = df.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    # Identify the bowler with the highest wickets in a single match between the two teams and the corresponding wickets.
    highest_wickets_bowler_name = df.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_wickets = df.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    # Filter the dataframe to calculate the highest and lowest team scores between the two teams.
    min_max_df = df[(df['WonBy'] != 'NoResults') & (df['method'] != 'D/L') & (df['innings'].isin([1, 2]))]
    temp_df = min_max_df.groupby(['ID', 'innings', 'BattingTeam'])['total_run'].sum().reset_index()

    # Identify the highest and lowest team scores between the two teams.
    highest_score_name = temp_df.sort_values('total_run', ascending=False).iloc[0]['BattingTeam']
    highest_score = temp_df.sort_values('total_run', ascending=False).iloc[0]['total_run']

    lowest_score_name = temp_df.sort_values('total_run').iloc[0]['BattingTeam']
    lowest_score = temp_df.sort_values('total_run').iloc[0]['total_run']

    # Identify the top 5 batsmen based on total runs in matches between the two teams.
    top_5_batsmen_names = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_batsmen_runs = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().values.tolist()

    # Identify the top 5 bowlers based on total wickets in matches between the two teams.
    top_5_bowlers_names = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_bowlers_wickets = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().values.tolist()

    # Calculate the number of matches won by each team and the number of drawn matches between them.
    matches_won_by_team1 = df[df['WinningTeam'] == team1]['ID'].unique().size
    matches_won_by_team2 = df[df['WinningTeam'] == team2]['ID'].unique().size
    matches_draw = df[df['WinningTeam'].isnull()]['ID'].unique().size

    # Structure the data for JSON response.
    data = {
        'teamVsTeamAllSeasons' : {
            'teamsName': {
                'team1Name': team1,
                'team2Name': team2
            },
            'totalSeasonsPlayed' : total_seasons_played,
            'totalMatchesPlayed': total_matches_played,
            'totalSuperOversPlayed' : total_super_overs_played,
            'highestRunsBatsmanName': highest_runs_batsman_name,
            'highestRuns': highest_runs,
            'highestWicketsBowlerName': highest_wickets_bowler_name,
            'highestWickets': highest_wickets,
            'highesScoreName': highest_score_name,
            'highesScore': highest_score,
            'lowestScoreName': lowest_score_name,
            'lowestScore': lowest_score,
            'top5Batsmen': {
                'names': top_5_batsmen_names,
                'runs': top_5_batsmen_runs
            },
            'top5Bowlers': {
                'names': top_5_bowlers_names,
                'wickets': top_5_bowlers_wickets
            },
            'matchesWinDraw' : {
                'matchesWonByTeam1': matches_won_by_team1,
                'matchesWonByTeam2': matches_won_by_team2,
                'matchesDraw': matches_draw
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def teamVsTeamSeasonAPI(team1, team2, season):
    # Filter the dataframe for matches where the specified teams played against each other in a given season.
    df = ball_with_match[(((ball_with_match['Team1'] == team1) & (ball_with_match['Team2'] == team2)) | ((ball_with_match['Team1'] == team2) & (ball_with_match['Team2'] == team1))) & (ball_with_match['Season'] == int(season))].copy()

    # Calculate the total number of unique matches the teams played against each other during the specified season.
    total_matches_played = df['ID'].unique().size

    # Calculate the total number of super overs played by the teams against each other during the specified season.
    total_super_overs_played = df[df['SuperOver'] == 'Y']['ID'].unique().size

    # Identify the batsman with the highest runs in a single match between the two teams during the specified season.
    highest_runs_batsman_name = df.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_runs = df.groupby(['batter', 'ID'])['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    # Identify the bowler with the highest wickets in a single match between the two teams during the specified season.
    highest_wickets_bowler_name = df.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).index[0][0]
    highest_wickets = df.groupby(['bowler', 'ID'])['isWicketDelivery'].sum().sort_values(ascending=False).head(1).values[0]

    # Filter the dataframe to calculate the highest and lowest team scores between the two teams during the specified season.
    min_max_df = df[(df['WonBy'] != 'NoResults') & (df['method'] != 'D/L') & (df['innings'].isin([1, 2]))]
    temp_df = min_max_df.groupby(['ID', 'innings', 'BattingTeam'])['total_run'].sum().reset_index()

    # Identify the highest and lowest team scores between the two teams during the specified season.
    highest_score_name = temp_df.sort_values('total_run', ascending=False).iloc[0]['BattingTeam']
    highest_score = temp_df.sort_values('total_run', ascending=False).iloc[0]['total_run']

    lowest_score_name = temp_df.sort_values('total_run').iloc[0]['BattingTeam']
    lowest_score = temp_df.sort_values('total_run').iloc[0]['total_run']

    # Identify all players from both teams who participated during the specified season.
    team1_players = sorted(set(df[df['BattingTeam'] == team1]['batter'].unique().tolist() + df[df['BattingTeam'] != team1]['bowler'].unique().tolist()))
    team2_players = sorted(set(df[df['BattingTeam'] == team2]['batter'].unique().tolist() + df[df['BattingTeam'] != team2]['bowler'].unique().tolist()))

    # Identify the top 5 batsmen based on total runs in matches between the two teams during the specified season.
    top_5_batsmen_names = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_batsmen_runs = df.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head().values.tolist()

    # Identify the top 5 bowlers based on total wickets in matches between the two teams during the specified season.
    top_5_bowlers_names = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().index.tolist()
    top_5_bowlers_wickets = df.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head().values.tolist()

    # Calculate the number of matches won by each team and the number of drawn matches between them during the specified season.
    matches_won_by_team1 = df[df['WinningTeam'] == team1]['ID'].unique().size
    matches_won_by_team2 = df[df['WinningTeam'] == team2]['ID'].unique().size
    matches_draw = df[df['WinningTeam'].isnull()]['ID'].unique().size

    # Structure the data for JSON response.
    data = {
        'teamVsTeamSeason' : {
            'teamsName' : {
                'team1Name' : team1,
                'team2Name' : team2
            },
            'totalMatchesPlayed': total_matches_played,
            'totalSuperOversPlayed' : total_super_overs_played,
            'highestRunsBatsmanName': highest_runs_batsman_name,
            'highestRuns': highest_runs,
            'highestWicketsBowlerName': highest_wickets_bowler_name,
            'highestWickets': highest_wickets,
            'highesScoreName': highest_score_name,
            'highesScore': highest_score,
            'lowestScoreName': lowest_score_name,
            'lowestScore': lowest_score,
            'players': {
                'team1Players': team1_players,
                'team2Players' : team2_players
            },
            'top5Batsmen': {
                'names': top_5_batsmen_names,
                'runs': top_5_batsmen_runs
            },
            'top5Bowlers': {
                'names': top_5_bowlers_names,
                'wickets': top_5_bowlers_wickets
            },
            'matchesWinDraw' : {
                'matchesWonByTeam1' : matches_won_by_team1,
                'matchesWonByTeam2' : matches_won_by_team2,
                'matchesDraw': matches_draw
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def batsmanAllSeasonsAPI(batsman):
    # Filter the dataframe to select data only for the specified batsman and valid innings.
    df = ball_with_match[(ball_with_match['batter'] == batsman) & ball_with_match['innings'].isin([1, 2])]

    # Calculate the total number of unique seasons in which the batsman played.
    total_seasons_played = df['Season'].unique().size

    # Calculate the total number of unique matches the batsman played.
    total_matches_played = df['ID'].unique().size

    # Calculate the batsman's total runs across all seasons.
    total_runs = df['batsman_run'].sum()

    # Calculate the total number of fours and sixes hit by the batsman.
    total_fours = df[df['batsman_run'] == 4].shape[0]
    total_sixes = df[df['batsman_run'] == 6].shape[0]

    # Calculate the number of times the batsman was out to determine batting average.
    total_out = df[df['player_out'] == batsman].shape[0]
    if total_out:
        average = round(total_runs / total_out, 2)
    else:
        average = np.inf

    # Calculate the total number of balls faced by the batsman, excluding wides to determine strike rate.
    total_balls_played = df[~(df['extra_type'] == 'wides')].shape[0]
    if total_balls_played:
        strike_rate = round((total_runs / total_balls_played) * 100, 2)
    else:
        strike_rate = 0

    # Group data by match to calculate runs per match and identify fifties and centuries.
    temp_df = df.groupby('ID').sum()

    total_fifties = temp_df[(temp_df['batsman_run'] >= 50 ) * (temp_df['batsman_run'] < 100)].shape[0]
    total_centuries = temp_df[temp_df['batsman_run'] >= 100 ].shape[0]

    # Identify the batsman's highest score across all matches.
    highest_score = temp_df['batsman_run'].sort_values(ascending=False).values[0]

    # Calculate the number of times the batsman was awarded the Player of the Match.
    total_mom = ball_with_match[ball_with_match['Player_of_Match'] == batsman]['ID'].unique().size

    # Identify the teams the batsman has played for, with the current team separated from past teams.
    teams_df = df['BattingTeam'].unique().tolist()
    playing_in = teams_df[0]
    played_in_teams = teams_df[1::]

    # Get the batsman's runs per season.
    seasons = df.groupby('Season')['batsman_run'].sum().index.tolist()
    season_wise_runs = df.groupby('Season')['batsman_run'].sum().values.tolist()

    # Structure the data for JSON response.
    data = {
        'batsmanAllSeasons': {
            'totalSeasonsPlayed' : total_seasons_played,
            'totalMatchesPlayed': total_matches_played,
            'totalRuns' : total_runs,
            'totalFours' : total_fours,
            'totalSixes' : total_sixes,
            'average': average,
            'strikeRate': strike_rate,
            'totalFifties': total_fifties,
            'totalCenturies': total_centuries,
            'highestScore': highest_score,
            'totalMOM': total_mom,
            'playingIn' : playing_in,
            'playedIn': {
                'teams': played_in_teams
            },
            'seasonWiseRuns': {
                'seasons': seasons,
                'runs': season_wise_runs
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def batsmanSeasonAPI(batsman, season):
    # Filter the dataframe for the specified batsman and season.
    df = ball_with_match[(ball_with_match['batter'] == batsman) & (ball_with_match['Season'] == int(season)) & (ball_with_match['innings'].isin([1, 2]))]

    # Calculate the number of matches the batsman played in the specified season.
    total_matches_played = df['ID'].unique().size

    # Calculate the total runs, fours, and sixes scored by the batsman in the season.
    total_runs = df['batsman_run'].sum()
    total_fours = df[df['batsman_run'] == 4].shape[0]
    total_sixes = df[df['batsman_run'] == 6].shape[0]

    # Calculate the number of times the batsman was out to determine batting average.
    total_out = df[df['player_out'] == batsman].shape[0]
    if total_out:
        average = round(total_runs / total_out, 2)
    else:
        average = np.inf

    # Calculate the strike rate (runs per 100 balls).
    total_balls_played = df[~(df['extra_type'] == 'wides')].shape[0]
    if total_balls_played:
        strike_rate = round((total_runs / total_balls_played) * 100, 2)
    else:
        strike_rate = 0

    # Group data by match to identify fifties and centuries.
    temp_df = df.groupby('ID').sum()
    total_fifties = temp_df[(temp_df['batsman_run'] >= 50) * (temp_df['batsman_run'] < 100)].shape[0]
    total_centuries = temp_df[temp_df['batsman_run'] >= 100].shape[0]

    # Identify the batsman's highest score in the specified season.
    highest_score = temp_df['batsman_run'].sort_values(ascending=False).values[0]

    # Calculate the number of Player of the Match awards won by the batsman in the season.
    total_mom = ball_with_match[ball_with_match['Player_of_Match'] == batsman]['ID'].unique().size

    # Identify the team that the batsman played for.
    batting_team = df['BattingTeam'].unique()[0]

    # Get a list of opposition teams the batsman played against in the season.
    teams = sorted(set(df[df['Team1'] != batting_team]['Team1'].tolist() + df[df['Team2'] != batting_team]['Team2'].tolist()))

    # Calculate the runs scored by the batsman against each team.
    runs = []
    for i in teams:
        temp_df = df[(df['Team1'] == i) | (df['Team2'] == i)]
        sum = temp_df.groupby('batter')['batsman_run'].sum().values[0]
        runs.append(sum)

    # Get a list of matches and corresponding runs scored in each match.
    matches = list(range(1, len(df.groupby('ID')['batsman_run'].sum()) + 1))
    match_wise_runs = df.groupby('ID')['batsman_run'].sum().values.tolist()

    # Structure the data for JSON response.
    data = {
        'batsmanSeason': {
            'totalMatchesPlayed': total_matches_played,
            'totalRuns': total_runs,
            'totalFours': total_fours,
            'totalSixes': total_sixes,
            'average': average,
            'strikeRate': strike_rate,
            'totalFifties': total_fifties,
            'totalCenturies': total_centuries,
            'highestScore': highest_score,
            'totalMOM': total_mom,
            'playingIn' : batting_team,
            'scoreAgainstAllTeams': {
                'teams': teams,
                'runs': runs
            },
            'seasonWiseRuns': {
                'matches': matches,
                'runs': match_wise_runs
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def bowlerAllSeasonsAPI(bowler):
    # Filter the dataframe for the specified bowler.
    df = ball_with_match[ball_with_match['bowler'] == bowler]

    # Calculate the number of seasons and matches the bowler played.
    total_seasons_played = df['Season'].unique().size
    total_matches_played = df['ID'].unique().size

    # Calculate the total wickets taken by the bowler.
    total_wickets = df['isBowlerWicket'].sum()

    # Calculate total balls bowled excluding wides and no-balls, and the total runs given by the bowler.
    total_balls = df[~(df.extra_type.isin(['wides', 'noballs']))].shape[0]
    total_runs = df['bowler_run'].sum()

    # Calculate the economy rate.
    if total_balls:
        economy = round((total_runs / total_balls) * 6, 2)
    else:
        economy = 0

    # Calculate the bowling average.
    if total_wickets:
        average = round(total_runs / total_wickets, 2)
    else:
        average = np.inf

    # Calculate the bowling strike rate.
    if total_wickets:
        strike_rate = round(total_balls / total_wickets, 2)
    else:
        strike_rate = np.nan

    # Calculate the number of fours and sixes hit off the bowler's bowling.
    total_fours = df[(df.batsman_run == 4) & (df.non_boundary == 0)].shape[0]
    total_sixes = df[(df.batsman_run == 6) & (df.non_boundary == 0)].shape[0]

    # Identify the best bowling figure.
    temp_df = df.groupby('ID').sum()
    best_wicket = temp_df.sort_values(['isBowlerWicket', 'bowler_run'], ascending=[False, True])[['isBowlerWicket', 'bowler_run']].head(1).values
    if best_wicket.size > 0:
        best_figure = f'{best_wicket[0][0]}/{best_wicket[0][1]}'
    else:
        best_figure = np.nan

    # Calculate the number of times the bowler took 3 or more wickets in a match.
    total_w3 = temp_df[(temp_df.isBowlerWicket >= 3)].shape[0]

    # Calculate the number of Player of the Match awards won by the bowler.
    total_mom = df[df.Player_of_Match == bowler].drop_duplicates('ID', keep='first').shape[0]

    # Identify the teams the bowler played for.
    teams_df = pd.Series(df[df['Team1'] != df['BattingTeam']]['Team1'].unique().tolist() + df[df['Team2'] != df['BattingTeam']]['Team2'].unique().tolist()).unique().tolist()
    playing_in = teams_df[0]
    played_in_teams = teams_df[1::]

    # Calculate wickets taken in each season.
    seasons = df.groupby('Season')['isBowlerWicket'].sum().index.tolist()
    season_wise_wickets = df.groupby('Season')['isBowlerWicket'].sum().values.tolist()

    # Structure the data for JSON response.
    data = {
        'bowlerAllSeasons': {
            'totalSeasonsPlayed' : total_seasons_played,
            'totalMatchesPlayed': total_matches_played,
            'totalWickets' : total_wickets,
            'economy' : economy,
            'average' : average,
            'strikeRate': strike_rate,
            'totalFours': total_fours,
            'totalSixes': total_sixes,
            'bestFigure': best_figure,
            'totalW3': total_w3,
            'totalMOM': total_mom,
            'playingIn' : playing_in,
            'playedIn': {
                'teams': played_in_teams
            },
            'seasonWiseWickets': {
                'seasons': seasons,
                'wickets': season_wise_wickets
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)

def bowlerSeasonAPI(bowler, season):
    # Filter the dataframe for the specified bowler and season.
    df = ball_with_match[(ball_with_match['bowler'] == bowler) & (ball_with_match['Season'] == int(season))]

    # Calculate the number of matches the bowler played during the specified season.
    total_matches_played = df['ID'].unique().size

    # Calculate the total wickets taken by the bowler during the specified season.
    total_wickets = df['isBowlerWicket'].sum()

    # Calculate total balls bowled excluding wides and no-balls, and the total runs given by the bowler during the specified season.
    total_balls = df[~(df.extra_type.isin(['wides', 'noballs']))].shape[0]
    total_runs = df['bowler_run'].sum()

    # Calculate the economy rate.
    if total_balls:
        economy = round((total_runs / total_balls) * 6, 2)
    else:
        economy = 0

    # Calculate the bowling average.
    if total_wickets:
        average = round(total_runs / total_wickets, 2)
    else:
        average = np.inf

    # Calculate the bowling strike rate.
    if total_wickets:
        strike_rate = round(total_balls / total_wickets, 2)
    else:
        strike_rate = np.nan

    # Calculate the number of fours and sixes hit off the bowler's bowling during the specified season.
    total_fours = df[(df.batsman_run == 4) & (df.non_boundary == 0)].shape[0]
    total_sixes = df[(df.batsman_run == 6) & (df.non_boundary == 0)].shape[0]

    # Identify the best bowling figure for the season.
    temp_df = df.groupby('ID').sum()
    best_wicket = temp_df.sort_values(['isBowlerWicket', 'bowler_run'], ascending=[False, True])[['isBowlerWicket', 'bowler_run']].head(1).values
    if best_wicket.size > 0:
        best_figure = f'{best_wicket[0][0]}/{best_wicket[0][1]}'
    else:
        best_figure = np.nan

    # Calculate the number of times the bowler took 3 or more wickets in a match during the specified season.
    total_w3 = temp_df[(temp_df.isBowlerWicket >= 3)].shape[0]

    # Calculate the number of Player of the Match awards won by the bowler during the specified season.
    total_mom = df[df.Player_of_Match == bowler].drop_duplicates('ID', keep='first').shape[0]

    # Identify the team the bowler played for during the specified season.
    bowling_team = df[df['Team1'] != df['BattingTeam']]['Team1'].unique()[0]
    teams = sorted(set(df[df['Team1'] != bowling_team]['Team1'].tolist() + df[df['Team2'] != bowling_team]['Team2'].tolist()))

    # Calculate wickets taken against each team during the specified season.
    wickets = []
    for i in teams:
        temp_df = df[(df['Team1'] == i) | (df['Team2'] == i)]
        sum = temp_df['isBowlerWicket'].sum()
        wickets.append(sum)

    # Structure data for the match-wise wickets taken.
    matches = list(range(1, len(df.groupby('ID')['batsman_run'].sum()) + 1))
    match_wise_wickets = df.groupby('ID')['isBowlerWicket'].sum().values.tolist()

    # Structure the data for JSON response.
    data = {
        'bowlerSeason': {
            'totalMatchesPlayed': total_matches_played,
            'totalWickets': total_wickets,
            'economy': economy,
            'average': average,
            'strikeRate': strike_rate,
            'totalFours': total_fours,
            'totalSixes': total_sixes,
            'bestFigure': best_figure,
            'totalW3': total_w3,
            'totalMOM': total_mom,
            'playingIn' : bowling_team,
            'wicketsAgainstAllTeams': {
                'teams': teams,
                'wickets': wickets
            },
            'matchesWiseWickets': {
                'matches': matches,
                'wickets': match_wise_wickets
            }
        }
    }

    # Return the data in JSON format.
    return json.dumps(data, cls=NpEncoder)