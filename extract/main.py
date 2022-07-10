"""
Extracts data from Motor Vehicle collision datasets
"""
import requests
from datetime import datetime
from config import NYC_OPEN_DATA_API_APP_TOKEN

from .models.crashes import CrashRecord
from .models.enums import DATA_SOURCES

base_urls = {
    "crashes": "https://data.cityofnewyork.us/resource/h9gi-nx95.json",
    "vehicles": "https://data.cityofnewyork.us/resource/bm4k-52h4.json"
}


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

    for key in base_urls:
        results = session.get(base_urls[key], params=params)
        min_date, max_date = map(datetime.fromisoformat, results.json()[0].values())

        # Update your dict
        result[key] = {
            "min_date": min_date,
            "max_date": max_date
        }

    return result


# Get min and max dates for each data source
# min_max_dates = get_min_and_max_dates(session)
def extract_data(
    data_source: DATA_SOURCES,
    extract_start_time: datetime = None,
    extract_end_time: datetime = None
    ):
    """
    Extract data from a given data source.

    Args:
        data_source: name of a data source you'd like to extract
        extract_start_time: (optional) lower bound limit to begin extraction
        extract_end_time: (optional) upper bound limit to conclude extraction
    """

    offset = 0
    increments = 50_000

    params={
        "$offset": offset,
        "$limit": increments,
        "$where": "vehicle_type_code1 = 'Sedan' and borough = 'BROOKLYN'"
    }

    all_records = []

    while True:


        # Let's paginate
        results = session.get(base_urls[data_source], params=params)
        data = results.json()

        # clean em up
        records = [CrashRecord.parse_obj(x) for x in data]

        # No records, you are at the end
        if not records:
            break

        # Save locally – in the cloud, we would save to S3
        all_records.extend(records)

        # Increase the offset count
        params["$offset"] += increments

        # print(records)

    # How many records u got?
    print(len(all_records))
