"""Responsible for loading data (from json) to the DB"""

import os
import json
from datetime import datetime, timedelta, timezone
from typing import List

from rich.progress import Progress
from logger import LOGGER, console


import models
from config import data_sources
from models.enums import DATA_SOURCES
from database import ConnectDb
from database import models as db_models


orm_models_mappings = {
    "crashes": {
        "orm_model": db_models.crashes.CrashRecord,
        "primary_key": "collision_id"
    }
}



class Loader:

    def __init__(self):
        self.state_path = 'load_state.json'
        self.state = self.get_state()
        self._session = None

    @property
    def session(self):
        if not self._session:
            self._session = ConnectDb().session
        return self._session


    def get_state(self):
        """
        Returns a dictionary of which files have been successfully
        loaded into the DB
        """

        if not os.path.isfile(self.state_path):
            return {}
        else:
            with open(self.state_path, 'r') as f:
                data = json.load(f)
            return data

    def save_state(self):
        """Saves current state to state path"""
        if self.state:
            with open(self.state_path, 'w') as f:
                json.dump(self.state, f, default=str)



    def load_data(self,
        data_source: DATA_SOURCES,
        start_time: datetime = (datetime.now(tz=timezone.utc) - timedelta(hours=24)),
        end_time: datetime = datetime.now(tz=timezone.utc)
        ) -> List:
        """
        Load data from a given data source.

        Args:
            data_source: name of a data source you'd like to extract
            start_time: lower bound limit to include files from
            end_time: upper bound limit to include files from
        """

        if data_source not in orm_models_mappings:
            LOGGER.warning(
                f"\"{data_source}\" has not been configured in the ORM yet. "
                f"Data is available locally, but cannot be loaded into the "
                f"database until later. Sorry about that."
            )
            return


        # Set up state properly
        if data_source not in self.state:
            self.state[data_source] = {}

        # Get the models to be used
        response_model = data_sources[data_source]["response_model"]
        orm_model = orm_models_mappings[data_source]["orm_model"]
        primary_key = orm_models_mappings[data_source]["primary_key"]

        # Get all the extraction dates for this data source
        base_path = f'data/{data_source}'
        extract_dates = [x for x in os.listdir(base_path) if x !='.DS_Store']

        visit_dirs = []
        # Which directories should you load?
        for path in extract_dates:
            extract_date = datetime.strptime(path, '%Y-%m-%d').replace(tzinfo=timezone.utc).date()
            if start_time.date() <= extract_date <= end_time.date():
                visit_dirs.append(f'{base_path}/{path}')

        # We will only get the most recent one – for now (fix later)
        visit_dir = max(visit_dirs)
        all_paths = os.listdir(visit_dir)

        with Progress(console=console) as progress:

            task = progress.add_task(f"Loading data into the DB for {data_source=}", total=len(all_paths))

            # Load the files in this directory
            for path in all_paths:
                file_path = f'{visit_dir}/{path}'

                # Don't visit the same file 2x
                if file_path in self.state[data_source]:
                    LOGGER.info(f'Already loaded contents from {file_path} to the db')
                    progress.advance(task)
                    continue

                # get the raw data
                with open(file_path, 'r') as f:
                    data = json.load(f)

                # Format the records
                records = [response_model.parse_obj(x) for x in data]
                primary_keys = [getattr(x, primary_key) for x in records]


                # Get records which already exist
                query = self.session.query(getattr(orm_model, primary_key))\
                    .where(getattr(orm_model, primary_key).in_(primary_keys))

                existing_records: set = {x[0] for x in query.all()}

                # Don't include records which already exist in the db
                orm_records = [orm_model(**x.dict()) for x in records
                    if getattr(x, primary_key) not in existing_records
                ]

                self.session.bulk_save_objects(orm_records)
                self.session.commit()

                # You've been here
                self.state[data_source][file_path] = datetime.now(tz=timezone.utc)
                self.save_state()
                LOGGER.info(f'Done saving contents from {file_path} to the db')
                progress.advance(task)
