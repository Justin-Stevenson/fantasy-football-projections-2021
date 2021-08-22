# import requests
# from bs4 import BeautifulSoup

# # download wikipage
# player_page = "https://www.nfl.com/players/patrick-mahomes/"
# result = requests.get(player_page)

# # if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
# if result.status_code == 200:
#     soup = BeautifulSoup(result.content, "html.parser")
    
# # find the object with HTML class wikitable sortable
# figure = soup.find('figure',{'class':'nfl-c-player-header__headshot'})
# image = figure.find('img', {'class':'img-responsive'})

# print(image['src'])