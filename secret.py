import json
import os
from pathlib import Path

creds_dir = Path(os.environ.get('CREDS_DIR'))
## Telegram
with open(creds_dir / Path('tg_token.json')) as file:
    TG_TOKEN = json.load(file)['token']

## Google sheets
G_CREDS = 'creds/creds.json'
with open(creds_dir / Path('gsheet.json')) as file:
    G_INFO = json.load(file)
    G_SHEETS_ID = G_INFO['G_SHEETS_ID']
    G_SCOPE = G_INFO['G_SCOPE']
