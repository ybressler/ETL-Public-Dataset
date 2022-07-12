"""Entry point for the application"""

from extract import main
from load.main import Loader
import json
import os

from config import data_sources

from models.crashes import CrashRecord

# base_path = 'data/crashes/2022-07-11'
# all_files = os.listdir(base_path)
# all_data = []
# for file in all_files:
#     with open(f'{base_path}/{file}', 'r') as f:
#         data = json.load(f)
#     all_data.extend(data)
#
#
# all_data = [CrashRecord.parse_obj(x) for x in all_data]


if __name__ =='__main__':

    # Eventually, will allow all sources
    for key in ["crashes"]:

        # Extract
        records = main.extract_data(key)

        # Save locally, a bit extra IO, but helps if
        # you want to break into discrete steps
        main.save_data(key, records)

        # Load the data into the DB
        loader = Loader()
        loader.load_data(key)
