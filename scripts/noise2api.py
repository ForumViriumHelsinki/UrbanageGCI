import copy
import csv
import json
import logging
import sys
from datetime import datetime

import httpx

# Set logging level to DEBUG to see debug messages
logging.basicConfig(level=logging.INFO)

API_URL = sys.argv[1]
API_HEADERS = {
    "Content-Type": "application/json",
    "Fiware-Service": "helsinki",
    "User-Agent": "UrbanAge noise2api/0.0.1",
}

locations = {
    "TA120-T246184": {  # Mäkelänkatu
        "location": {
            "coordinates": [24.952025, 60.196394],
            "type": "Point"
        }
    },
    "TA120-T246191": {  # Kalevankatu 39
        "location": {
            "coordinates": [24.931362, 60.16513],
            "type": "Point"
        }
    },
    "TA120-T246187": {  # Lapinlahden sairaala
        "location": {
            "coordinates": [24.911846, 60.168094],
            "type": "Point"
        }
    },
}

noise_template = {
    "dBA": 24.9,
    "dateObservedFrom": "2023-07-06T08:00:00Z",
    "dateObservedTo": "2023-07-06T08:00:00Z",
    "dev_id": 1,
    "id": "0",
    "location": {
        "coordinates": [
            "24.9506",
            "60.18739"
        ],
        "type": "Point"
    },
    "type": "NoiseLevelObserved"
}

sample_csv_data = """time,readable_time,dBA,dev-id
1693993704000,2023-09-06T09:48:24Z,43.8,TA120-T246183
1693993705000,2023-09-06T09:48:25Z,65.9,TA120-T246191
1693993734000,2023-09-06T09:48:54Z,68.2,TA120-T246184
1693993761000,2023-09-06T09:49:21Z,61.1,TA120-T246187
1693993764000,2023-09-06T09:49:24Z,43.8,TA120-T246183
1693993765000,2023-09-06T09:49:25Z,65.2,TA120-T246191
"""


# Function to convert timestamp to readable time format
def timestamp_to_readable_time(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_csv_data(url: str) -> list:
    # Fetch the CSV data from the URL
    response = httpx.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the CSV data
        csv_data = response.text.splitlines()
        csv_reader = csv.DictReader(csv_data)
        noises = []
        for row in csv_reader:
            # Convert time and dBA to numbers
            row["time"] = int(row["time"])
            row["dBA"] = float(row["dBA"])
            row["dev-id"] = row["dev-id"]
            noises.append(row)
        return noises


def preserve_latest_noise(noises: list) -> list:
    # Create a dictionary to store the latest timestamp for each dev-id
    latest_timestamps = {}

    # Iterate through the data and update the latest timestamps
    for entry in noises:
        dev_id = entry['dev-id']
        timestamp = entry['time']

        if dev_id not in latest_timestamps or timestamp > latest_timestamps[dev_id]:
            latest_timestamps[dev_id] = timestamp

    # Create a new list with only the entries corresponding to the latest timestamps
    filtered_data = [entry for entry in noises if entry['time'] == latest_timestamps[entry['dev-id']]]
    return filtered_data


def create_post_data(noise: dict):
    # Create a copy of the template using copy.deepcopy
    p = copy.deepcopy(noise_template)
    # Update the id
    if noise['dev-id'] in locations:
        p["dev_id"] = noise['dev-id']
        # Update the location
        p["location"] = locations[noise['dev-id']]["location"]
        p["dBA"] = noise["dBA"]
        p["dateObservedFrom"] = p["dateObservedTo"] = timestamp_to_readable_time(noise["time"])
        return p
    else:
        return None


def post_data(p: dict):
    body = json.dumps(p, indent=2)
    logging.debug(body)
    # print(body)
    res = httpx.post(API_URL, json=p, headers=API_HEADERS)
    return res


def main():
    # Get uiras data from url using httpx
    url = "https://iot.fvh.fi/downloads/noise/tmp/last_minute.csv"
    noises = get_csv_data(url)
    noises = preserve_latest_noise(noises)
    for n in noises:
        pl = create_post_data(n)
        if pl is not None:
            res = post_data(pl)
            logging.info(f"Sent {pl}, status: {res.status_code} {res.text}")


if __name__ == "__main__":
    main()
