import pandas as pd
import pyppeteer
import asyncio

URL = "https://www.basketball-reference.com/teams/{}/{}.html"

async def get_roster(team, season):
  browser = await pyppeteer.launch()
  page = browser.newPage()
  await page.goto(f"https://www.basketball-reference.com/teams/{team}/{season}.html")
  await page.waitForSelector('#roster')
  table = await page.querySelectorEval('#roster', '(element) => element.outerHTML')
  await browser.close()
  return pd.read_html(table)[0]

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  df = loop.run_until_complete(get_roster('GSW','2021'))
  loop.close()
  print(df)