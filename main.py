"""Entry point for the application"""

from extract import main
import json
import os

from extract.models.crashes import CrashRecord

# base_path = 'data/crashes/2022-07-11'
# all_files = os.listdir(base_path)
# all_data = []
# for file in all_files:
#     with open(f'{base_path}/{file}', 'r') as f:
#         data = json.load(f)
#     all_data.extend(data)
#
# all_data = [CrashRecord.parse_obj(x) for x in all_data]


if __name__ =='__main__':
    records = main.extract_data("crashes")
    main.save_data("crashes", records)
