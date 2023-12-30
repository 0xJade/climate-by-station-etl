from etl.etl import *
import json
import pandas as pd
from io import StringIO

report = {}

def main():
    # Read the NOAAConfig.js file into a dictionary
    with open('NOAAConfig.json') as f:
        config = json.load(f)

    url = config['daily_summaries_endpoint']

    for k, v in config['stations'].items():

        station_id = v['station_id']
        csv_data = StringIO(extract_data(f'{url}/{station_id}.csv'))
        df = pd.read_csv(csv_data)[['DATE','PRCP','TMIN']]
        report[k] = transform_data(df, config['years'], k, v['min_frozen'])

    load_data(f'./Climate Report {datetime.datetime.now().month}-{datetime.datetime.now().year}.pdf', report)

    print(report)

        # Transform the data

main()