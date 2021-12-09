import pandas as pd
import asyncio
from pyppeteer import launch
from basketball_reference_scraper.teams import get_roster, get_roster_stats, get_team_misc, get_opp_series, get_team_series
from basketball_reference_scraper.players import get_stats

if __name__ == '__main__':
  df = get_roster('GSW', '2021')
  for i in range(len(df)):
    player = get_stats(df.at[i,'PLAYER'],stat_type='PER_GAME')
    print(player)
