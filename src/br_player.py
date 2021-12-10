import pandas as pd
from pyppeteer import launch
import requests
from bs4 import BeautifulSoup
from src.br_constants import *
from src.br_team import get_roster
from src.br_uploader import *
import asyncio

try:
    from src.br_utils import get_player_suffix
except:
    from basketball_reference_scraper.utils import get_player_suffix

async def get_player_selector(suffix, selector):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com/{suffix}')
    await page.waitForSelector(f'{selector}')
    table = await page.querySelectorEval(f'{selector}', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table)[0]

def get_stats(name, stat_type='PER_GAME', playoffs=False, career=False):
    suffix = get_player_suffix(name)
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_'+selector
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_player_selector(suffix, '#'+selector))
    df = loop.run_until_complete(future)
    loop.close()
    career_index = df[df['Season']=='Career'].index[0]
    if career:
        df = df.iloc[career_index+2:, :]
    else:
        df = df.iloc[:career_index, :]

    df = df.dropna(axis=1)
    # loop.close()
    return df

def get_roster_stats(players):
    suffix = []
    for i in range(len(players)):
        suffix.append(get_player_suffix(players.at[i,'PLAYER']))
    suffix = pd.DataFrame(suffix, columns=['Suffix'])
    return suffix
    
def get_player_maps(team):
    URL = 'basketball-reference.com/teams/{}/2022.html'
    df = pd.DataFrame()
    roster = get_roster(team, 2022)
    roster = roster[['PLAYER']]
    for i in range(len(roster)):
        try:
            roster.loc[[i],['PLAYER']] = str(roster.at[i,'PLAYER']).replace(' (TW)','')
        except:
            pass
    suffix = get_roster_stats(roster)
    roster = pd.concat([roster, suffix], axis=1)
    df = pd.concat([df, roster], axis=0)
    return df