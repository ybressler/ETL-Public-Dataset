"""
Loads configuration

NOTE: This configuration file loads the following [environment] variables:
    * NYC_OPEN_DATA_API_APP_TOKEN
    * NYC_OPEN_DATA_API_APP_SECRET_TOKEN

For this configuration parser to work, you must do the following:
    1. Create a file `secrets/local.ini`
    2. Add the following to the file:
    ```
    [nyc_open_data]
    APP_TOKEN=****
    APP_SECRET_TOKEN=****
    ```
"""
import os
import configparser


STAGE = os.environ.get('STAGE', 'local')
secrets_path = f'secrets/{STAGE}.ini'

# Don't allow loading when ini doesn't exist
if not os.path.isfile(secrets_path):
    raise FileNotFoundError(f'{secrets_path} not found in {STAGE} environment')

cfg = configparser.ConfigParser()
cfg.read(secrets_path)

# NYC_OPEN_DATA_API_KEY_ID = cfg['nyc_open_data']['api_key_id']
# NYC_OPEN_DATA_API_KEY_SECRET = cfg['nyc_open_data']['api_key_secret']

NYC_OPEN_DATA_API_APP_TOKEN = cfg['nyc_open_data']['app_token']
NYC_OPEN_DATA_API_APP_SECRET_TOKEN = cfg['nyc_open_data']['app_secret_token']
