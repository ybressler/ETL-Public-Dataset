"""
Extracts data from Motor Vehicle collision datasets

ToDo:
    Add a logging agent
"""
import os
import json
from datetime import datetime, timezone
import requests
from typing import List

from config import NYC_OPEN_DATA_API_APP_TOKEN, data_sources
import models
from models.enums import DATA_SOURCES



# data_date_range = {}

# Prepare a session (reusable params)
session = requests.Session()
session.headers = {"X-App-Token": NYC_OPEN_DATA_API_APP_TOKEN}

def get_min_and_max_dates(session: requests.Session):
    """
    Get the min and max date
    Sometimes they are 1 or 2 days behind each other
    """
    result = {}
    params={
        "$select":"MIN(crash_date), MAX(crash_date)"
    }

    for key in data_sources:
        results = session.get(data_sources[key]["api_endpoint"], params=params)
        min_date, max_date = map(datetime.fromisoformat, results.json()[0].values())

        # Update your dict
        result[key] = {
            "min_date": min_date,
            "max_date": max_date
        }

    return result


def extract_data(
    data_source: DATA_SOURCES,
    extract_start_time: datetime = None,
    extract_end_time: datetime = None
    ) -> List:
    """
    Extract data from a given data source.

    Args:
        data_source: name of a data source you'd like to extract
        extract_start_time: (optional) lower bound limit to begin extraction
        extract_end_time: (optional) upper bound limit to conclude extraction
    """

    offset = 0
    increments = 50_000

    params = {
        "$offset": offset,
        "$limit": increments
    }

    api_endpoint = data_sources[data_source]["api_endpoint"]
    response_model = data_sources[data_source]["response_model"]

    all_records = []
    while True:

        results = session.get(api_endpoint, params=params)
        data = results.json()

        # clean em up
        records = [response_model.parse_obj(x) for x in data]

        # No records, you are at the end
        if not records:
            break

        all_records.extend(records)

        # Increase the offset count
        params["$offset"] += increments

    # How many records u got?
    return all_records


def save_data(data_source: DATA_SOURCES, records: List):
    """
    Saves data locally – in the cloud, we would save to S3

    Args:
        data_source: name of a data source you'd like to extract
        records: List of records to save

    ToDo: In the future, provide more options to save the data.
    """

    records = [x.dict() for x in records]

    curr_datetime = datetime.now(timezone.utc)
    curr_datetime_path = curr_datetime.strftime('%Y-%m-%d/%H-%M-%S')
    save_path = f'./data/{data_source}/{curr_datetime_path}'

    # Make the path
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    i = 1
    n_records_per_file = 50_000
    while records:
        file_path = f'{save_path}_part_{i}.json'
        with open(file_path, 'w') as f:
            json.dump(records[:n_records_per_file], f, default=str)

        # Iterate
        if n_records_per_file >= len(records):
            break
        else:
            records = records[n_records_per_file:]
            i += 1
