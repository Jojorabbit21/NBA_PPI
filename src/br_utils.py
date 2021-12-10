from requests import get
from bs4 import BeautifulSoup

def get_game_suffix(date, team1, team2):
    r = get(f'https://www.basketball-reference.com/boxscores/index.fcgi?year={date.year}&month={date.month}&day={date.day}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'class': 'teams'}):
            for anchor in table.find_all('a'):
                if 'boxscores' in anchor.attrs['href']:
                    if team1 in anchor.attrs['href'] or team2 in anchor.attrs['href']:
                        suffix = anchor.attrs['href']
    return suffix

def get_player_suffix(name):
    name_s = name.split(' ')
    if len(name_s) > 2:
      last_name = " ".join(name_s[-2:])
    else:
      last_name = name_s[-1]
    initial = last_name[0].lower()
    r = get(f'https://www.basketball-reference.com/players/{initial}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'id': 'players'}):
            for anchor in table.find_all('a'):
                if anchor.text==name:
                    return anchor.attrs['href']
