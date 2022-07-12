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

    [database]
    DB_URI=****
    ```
"""
import os
import configparser
import models

STAGE = os.environ.get('STAGE', 'local')
secrets_path = f'secrets/{STAGE}.ini'

# Don't allow loading when ini doesn't exist
if not os.path.isfile(secrets_path):
    raise FileNotFoundError(f'{secrets_path} not found in {STAGE} environment')

cfg = configparser.ConfigParser()
cfg.read(secrets_path)

# get API connection
NYC_OPEN_DATA_API_APP_TOKEN = cfg['nyc_open_data']['app_token']
NYC_OPEN_DATA_API_APP_SECRET_TOKEN = cfg['nyc_open_data']['app_secret_token']

# Get DB connection
DB_URI = cfg['database'].get('DB_URI', 'postgresql://postgres:@localhost:5430/db')


data_sources = {
    "crashes": {
        "api_endpoint": "https://data.cityofnewyork.us/resource/h9gi-nx95.json",
        "response_model": models.crashes.CrashRecord
    },
    "vehicles": {
        "api_endpoint": "https://data.cityofnewyork.us/resource/bm4k-52h4.json",
        "response_model": models.vehicles.CrashVehicleRecord
    },
    "person": {
        "api_endpoint": "https://data.cityofnewyork.us/resource/f55k-p6yu.json",
        "response_model": models.person.CrashPersonRecord
    },
}
