import gspread
from gspread_dataframe import set_with_dataframe

DB_NAME = 'NBA PPI'
DB_SHEETS = {
  "PMAP": 'Players',
  "STAT": 'Stats',
  "STAT_A": 'Stats_Advanced',
  "TEAM": 'Teams',
  "TEAM_A": 'Teams_Advanced',
  'M': 'Starters' 
}
DB_START_COL = {
  'PMAP': 2,
  'STAT': 2,
  'STAT_A': 2,
  'TEAM': 1,
  "TEAM_A": 1,
  'M': 1
}

def upload_dataframes(data, keyword, index=True, columns=True):
  gc = gspread.service_account(filename="./src/agent.json")
  sh = gc.open(DB_NAME).worksheet(DB_SHEETS[keyword])
  try:
    DB_START_ROW = int(sh.cell(1,1).value)
  except:
    DB_START_ROW = 1
  set_with_dataframe(sh, data, row=DB_START_ROW, col=DB_START_COL[keyword], include_index=index, include_column_header=columns)

def clear_sheet(sheetname, range=None):
  gc = gspread.service_account(filename="./src/agent.json")
  sh = gc.open(DB_NAME).worksheet(DB_SHEETS[sheetname])
  if range is None:
    sh.clear()
  else:
    sh.batch_clear([range])