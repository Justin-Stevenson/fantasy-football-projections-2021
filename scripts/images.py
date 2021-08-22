import io
import json
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

T_LAZY = "/t_lazy"
EMPTY = ""
SPACE = " "
DASH = "-"
PERIOD = "."
APOSTROPHE = "'"
ROOKIES = {
        'Trevor Lawrence': 'https://www.espn.com/nfl/player/_/id/4360310/trevor-lawrence',
        'Zach Wilson': 'https://www.espn.com/nfl/player/_/id/4361259/zach-wilson',
        'Trey Lance': 'https://www.espn.com/nfl/player/_/id/4383351/trey-lance',
        'Javonte Williams': 'https://www.espn.com/nfl/player/_/id/4361579/javonte-williams',
        'Travis Etienne': 'https://www.espn.com/nfl/player/_/id/4239996/travis-etienne-jr',
        'Trey Sermon': 'https://www.espn.com/nfl/player/_/id/4241401/trey-sermon',
        'DeVonta Smith': 'https://www.espn.com/nfl/player/_/id/4241478/devonta-smith',
        'Kyle Pitts': 'https://www.espn.com/nfl/player/_/id/4360248/kyle-pitts',
        'Irv Smith Jr.': 'https://www.espn.com/nfl/player/_/id/4040980/irv-smith-jr'
    }
TEAMS = {
    'Rams': 'Los Angeles Rams', 
    'Steelers': 'Pittsburgh Steelers', 
    'Buccaneers': 'Tampa Bay Buccaneers', 
    'Football Team': 'Washington Football Team', 
    'Bills': 'Buffalo Bills', 
    'Dolphins': 'Miami Dolphins', 
    'Cowboys': 'Dallas Cowboys', 
    'Colts': 'Indianapolis Colts', 
    'Eagles': 'Philadelphia Eagles', 
    'Cardinals': 'Arizona Cardinals', 
    'Panthers': 'Carolina Panthers', 
    'Packers': 'Green Bay Packers', 
    '49ers': 'San Francisco 49ers', 
    'Chiefs': 'Kansas City Chiefs', 
    'Browns': 'Cleveland Browns', 
    'Saints': 'New Orleans Saints', 
    'Ravens': 'Baltimore Ravens', 
    'Giants': 'New York Giants', 
    'Broncos': 'Denver Broncos', 
    'Patriots': 'New England Patriots', 
    'Seahawks': 'Seattle Seahawks', 
    'Falcons': 'Atlanta Falcons', 
    'Bears': 'Chicago Bears', 
    'Jets': 'New York Jets', 
    'Titans': 'Tennessee Titans', 
    'Chargers': 'Los Angeles Chargers', 
    'Vikings': 'Minnesota Vikings', 
    'Jaguars': 'Jacksonville Jaguars', 
    'Raiders': 'Las Vegas Raiders', 
    'Lions': 'Detroit Lions', 
    'Texans': 'Houston Texans', 
    'Bengals': 'Cincinnati Bengals'
}

def read_json_from_file(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def get_filename(position):
    return position.lower() + '.json'

def fix_player_name(player):
    if player['player'] == 'Laviska Shenault':
        player['player'] = 'Laviska Shenault Jr.'
    elif player['player'] == 'Henry Ruggs':
        player['player'] = 'Henry Ruggs III'
    elif player['player'] == 'Jeffery Wilson':
        player['player'] = 'Jeff Wilson'
    elif player['player'] == 'LeVeon Bell':
        player['player'] = "Le'Veon Bell"
    elif player['player'] == 'Kaimi Fairbairn':
        player['player'] = "Ka'imi Fairbairn"
    elif player['player'] == 'Irv Smith Jr.':
        player['player'] = 'Irv Smith'
    elif player['player'] == 'Redskins':
        player['player'] = 'Football Team'

def get_player_resource_name(name):
    if name == "DK Metcalf":
        name = "D K Metcalf"
    elif name == "AJ Dillon":
        name = "A J Dillon"
    elif name.endswith(PERIOD):
        name = name[:-1]
    elif name in TEAMS:
        name = TEAMS[name]
    
    hyphenated_name = name \
        .replace(PERIOD + SPACE, DASH) \
        .replace(SPACE, DASH) \
        .replace(PERIOD, DASH) \
        .replace(APOSTROPHE, DASH)
    
    return hyphenated_name.lower()

def get_player_profiler_url(player):
    return f"https://www.playerprofiler.com/nfl/{player['resource_name']}/"

def get_nfl_profile_url(player):
    return f"https://www.nfl.com/players/{player['resource_name']}/"

def get_teams_profile_url(team):
    return f"https://www.nfl.com/teams/{team['resource_name']}/"

def download_profile_page(item, url):
    result = requests.get(url, allow_redirects=False)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
    else:
        print(f"{item['player']} [{item['resource_name']}]: Unable to get player page [Code: {result.status_code} -- Url: {url}]")
        soup = None
    
    return soup

def extract_player_image_src_from_player_profiler_page(player_page):
    core = player_page.find(id='core')
    image = core.find('img', {'class':'w-full h-auto relative z-10'})
    
    return image['src']

def extract_player_image_src_from_nfl_player_page(player_page):
    figure = player_page.find('figure',{'class':'nfl-c-player-header__headshot'})
    image = figure.find('img', {'class':'img-responsive'})
    
    return image['src']

def extract_team_image_src_from_nfl_team_page(team_page):
    figure = team_page.find('figure',{'class':'nfl-c-team-header__logo'})
    image = figure.find('img', {'class':'img-responsive'})
    
    return image['src']

def execute(position):
    filename = get_filename(position)
    players = read_json_from_file(filename)

    for player in players:
        fix_player_name(player)
        resource_name = get_player_resource_name(player['player'])
        player['resource_name'] = resource_name

        if player['player'] in ROOKIES:
            player_url = get_player_profiler_url(player)
            player_page = download_profile_page(item=player, url=player_url)
            player_img_src = extract_player_image_src_from_player_profiler_page(player_page)
        elif player['player'] in TEAMS:
            team_url = get_teams_profile_url(player)
            team_page = download_profile_page(item=player, url=team_url)
            player_img_src = extract_team_image_src_from_nfl_team_page(team_page)
        else:
            player_url = get_nfl_profile_url(player)
            player_page = download_profile_page(item=player, url=player_url)
            player_img_src = extract_player_image_src_from_nfl_player_page(player_page)
        
        if player_img_src is None:
            player_img_src = ''
            print(f"{player['player']}: Unable to get player image src")
        else:
            player_img_src = remove_t_lazy_from_url(player_img_src)
            save_image(item=player, url=player_img_src)
            player['orig_img_src'] = player_img_src

    # write_json_to_file(data=players, filename='all.json')

def remove_t_lazy_from_url(url):
    return url.replace(T_LAZY, EMPTY)

def save_image(item, url):
    try:
        url = remove_t_lazy_from_url(url)
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        filepath = f"{os.getcwd()}/images/{item['pos'].lower()}/{item['resource_name']}.jpg"
        image.save(filepath, "JPEG", quality=95)
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
        print(f"{item['player']}: Unable to save player image")

def write_json_to_file(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


execute("ALL-PLAYERS")