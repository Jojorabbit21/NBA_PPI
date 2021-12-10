import gspread
from gspread_dataframe import set_with_dataframe

DB_NAME = 'NBA PPI'
DB_SHEETS = {
  "PMAP": 'Players',
  "STAT": 'Stats',
  "TEAM": 'Teams'
}
DB_START_COL = {
  'PMAP': 2,
  'STAT': 1,
  'TEAM': 1
}

def upload_dataframes(data, keyword, index=True, columns=True):
  gc = gspread.service_account(filename="./src/agent.json")
  sh = gc.open(DB_NAME).worksheet(DB_SHEETS[keyword])
  try:
    DB_START_ROW = int(sh.cell(1,1).value)
  except:
    DB_START_ROW = 1
  set_with_dataframe(sh, data, row=DB_START_ROW, col=DB_START_COL[keyword], include_index=index, include_column_header=columns)

def clear_sheet(sheetname):
  gc = gspread.service_account(filename="./src/agent.json")
  sh = gc.open(DB_NAME).worksheet(DB_SHEETS[sheetname])
  sh.clear()