import json

def read_json_from_file(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def get_filname(position):
    return position.lower() + '.json'

def print_out_team_dict(teams):
    teams_dict = {}
    for team in teams:
        teams_dict[team['player']] = ""
    
    print(teams_dict)

def get_teams(position):
    filename = get_filname(position)
    teams = read_json_from_file(filename)
    print_out_team_dict(teams)

get_teams("DST")