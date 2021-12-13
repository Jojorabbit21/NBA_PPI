import requests
import json as js
import pandas as pd
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from requests.api import head
from src.br_uploader import *

todays_games_url = 'https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2021/scores/00_todays_scores.json'
starters_url = 'https://stats.nba.com/js/data/leaders/00_active_starters_{}.json'

team_adv_url = 'https://www.basketball-reference.com/leagues/NBA_2022.html#all_advanced_team'

data_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo=&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='

trad_url = 'https://stats.nba.com/stats/leaguedashplayerstats?' \
          'College=&Conference=&Country=&DateFrom=&DateTo=&' \
          'Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&' \
          'Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&' \
          'Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N' \
          '&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&' \
          'PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&' \
          'ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='  
             
adv_url = 'https://stats.nba.com/stats/leaguedashplayerstats?' \
          'College=&Conference=&Country=&DateFrom=&DateTo=&' \
          'Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&' \
          'Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&' \
          'Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N' \
          '&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&' \
          'PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&' \
          'ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
        
games_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Dnt': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en',
    'origin': 'http://stats.nba.com',
    'Referer': 'https://github.com'
}
   
data_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    'Accept-Language': 'en-us',
    'Referer': 'https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1&Season=2019-20&SeasonType=Regular%20Season',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}

team_id = { # NBA.STAT ID TO ABR
  '1610612737':	'ATL',
  '1610612738':	'BOS',
  '1610612751':	'BRK',
  '1610612766':	'CHO',
  '1610612741':	'CHI',
  '1610612739':	'CLE',
  '1610612742':	'DAL',
  '1610612743':	'DEN',
  '1610612765':	'DET',
  '1610612744':	'GSW',
  '1610612745':	'HOU',
  '1610612754':	'IND',
  '1610612746':	'LAC',
  '1610612747':	'LAL',
  '1610612763':	'MEM',
  '1610612748':	'MIA',
  '1610612749':	'MIL',
  '1610612750':	'MIN',
  '1610612740':	'NOP',
  '1610612752':	'NYK',
  '1610612760':	'OKC',
  '1610612753':	'ORL',
  '1610612755':	'PHI',
  '1610612756':	'PHO',
  '1610612757':	'POR',
  '1610612758':	'SAC',
  '1610612759':	'SAN',
  '1610612761':	'TOR',
  '1610612762':	'UTA',
  '1610612764':	'WAS',
}

def get_player_stats():
  print("GET PLAYER STATS")
  print("CLEARING SHEETS")
  clear_sheet('STAT','B1:CC')
  js = get_json_data(trad_url)
  df = to_data_frame(js)
  print("PLAYERS STATS COLLECTED")
  df.sort_values(by=['TEAM_ABBREVIATION'], axis=0, inplace=True)
  print("UPLOADING PLAYER STATS")
  upload_dataframes(df,'STAT',index=False,columns=True)
  print("GET PLAYER STATS DONE")

def get_player_advanced_stats():
  print("GET PLAYER ADVANCED STATS")
  print("CLEARING SHEETS")
  clear_sheet('STAT_A','B1:CC')
  js = get_json_data(adv_url)
  df = to_data_frame(js)
  print("PLAYER ADVANCED STATS COLLECTED")
  df.sort_values(by=['TEAM_ABBREVIATION'], axis=0, inplace=True)
  print("UPLOADING PLAYER ADVANCED STATS")
  upload_dataframes(df,'STAT_A',index=False,columns=True)
  print("GET PLAYER ADVANCED STATS DONE")

def get_team_adv():
  raw = requests.get(team_adv_url)
  html = raw.text
  df = pd.read_html(html,match='Advanced')[0]
  print("GET TEAM ADVANCED STATS")
  df.columns = df.columns.droplevel()
  df = df.drop(['Rk','Unnamed: 17_level_1','Unnamed: 22_level_1','Unnamed: 27_level_1','Attend.','Attend./G'], axis=1)
  df = df.drop(30, axis=0)
  df.sort_values(by=['Team'],axis=0,inplace=True)
  print("TEAM ADVANCED STATS COLLECTED")
  print("CLEARING SHEETS")
  clear_sheet('TEAM_A','A1:Y31')
  print("UPLOADING TEAM ADVANCED STATS")
  upload_dataframes(df,'TEAM_A',index=False, columns=True)
  print("GET TEAM ADVANCED STATS DONE")

def get_team_stats():
  print("GET TEAM STATS")
  print("CLEARING SHEETS")
  clear_sheet('TEAM')
  js = get_json_data(data_url)
  df = to_data_frame(js)
  print("TEAM STATS COLLECTED")
  print("UPLOADING TEAM STATS")
  upload_dataframes(df,'TEAM',index=False,columns=True)
  print("GET TEAM STATS DONE")

def get_json_data(url):
    raw_data = requests.get(url, headers=data_headers)
    json = raw_data.json()
    return json.get('resultSets')
  
def get_todays_games_json(url):
    raw_data = requests.get(url, headers=games_header)
    json = raw_data.json()
    return json.get('gs').get('g')

def to_data_frame(data):
    data_list = data[0]
    df = pd.DataFrame(data=data_list.get('rowSet'), columns=data_list.get('headers'))
    return df

def get_starting_lineups(): #WIP
    print("GET MATCHUPS AND STARTING LINEUPS")
    td = datetime.now()
    est = td - timedelta(hours=14)
    fd = est.strftime('%Y%m%d')
    url = starters_url.format(fd)
    raw_data = requests.get(url, headers=games_header)
    json = raw_data.json()
    keys = json.keys()
    match_info = []
    print("MATCHUP & LINEUP COLLECTED")
    print('SANITIZING')
    for i in keys:
      single = []
      single.append(json[i]['htmid'])
      single.append(json[i]['vtmid'])
      if len(json[i]['htm']) > 0:
        for j in range(0,20):
          try:
            single.append(json[i]['htm'][j]['pid'])
          except:
            single.append("")
      if len(json[i]['vtm']) > 0:
        for j in range(0,20):
          try:
            single.append(json[i]['vtm'][j]['pid'])
          except:
            single.append("")
      match_info.append(single)
    df = pd.DataFrame(data=match_info)
    print("CLEARING SHEETS")
    clear_sheet('M','A2:AL20')
    print('UPLOADING MATCHUPS AND LINEUPS')
    upload_dataframes(df, 'M', index=False, columns=False)
    print("GET MATCHUPS AND LINEUPS DONE")

def main():
  get_player_stats()
  #get_player_advanced_stats()
  #get_starting_lineups()
  #get_team_adv()
  #get_team_stats()

# Start
main()

