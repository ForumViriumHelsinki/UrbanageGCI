import copy
import datetime
import json
import logging
import sys

import httpx
from fmiopendata.wfs import download_stored_query

# Set logging level to DEBUG to see debug messages
logging.basicConfig(level=logging.INFO)

API_URL = sys.argv[1]
API_HEADERS = {
    "Content-Type": "application/json",
    "Fiware-Service": "helsinki",
    "User-Agent": "UrbanAge fmi_aq2api/0.0.1",
}

# Source: https://ropengov.github.io/fmi2/articles/weather_observation_data.html
aq_stations = """4	Helsinki Kallio 2	100662	Kolmannen osapuolen ilmanlaadun havaintoasema	60.18739	24.9506	4258	1999-01-01T00:00:00Z	now
9	Helsinki Mannerheimintie	100742	Kolmannen osapuolen ilmanlaadun havaintoasema	60.16964	24.93924	4258	2005-01-04T00:00:00Z	now
11	Helsinki Mäkelänkatu	100762	Kolmannen osapuolen ilmanlaadun havaintoasema	60.19644	24.95198	4258	2015-01-27T00:00:00Z	now
13	Helsinki Vartiokylä Huivipolku	100803	Kolmannen osapuolen ilmanlaadun havaintoasema	60.22393	25.10244	4258	2009-01-22T00:00:00Z	now
341	Helsinki Katajanokka 2	104053	Kolmannen osapuolen ilmanlaadun havaintoasema	60.16522	24.973811	4258	2009-01-02T00:00:00Z	now
353	Helsinki Töölöntulli	104105	Kolmannen osapuolen ilmanlaadun havaintoasema	60.19034	24.915731	4258	2006-01-02T00:00:00Z	now
377	Helsinki Länsisatama 4	106948	Kolmannen osapuolen ilmanlaadun havaintoasema	60.15521	24.92178	4258	2019-01-01T00:00:00Z	now
379	Helsinki Pirkkola	106950	Kolmannen osapuolen ilmanlaadun havaintoasema	60.23422	24.92232	4258	2019-01-01T00:00:00Z	now
393	Helsinki Paloheinä	107165	Kolmannen osapuolen ilmanlaadun havaintoasema	60.25004	24.93942	4258	2019-01-01T00:00:00Z	now
"""

post_template = {
    "id": "fmi-100742",
    "type": "AirQualityObserved",
    "address": {"addressCountry": "FI", "addressLocality": "Helsinki", "streetAddress": "Mannerheimintie"},
    "location": {"type": "Point", "coordinates": [24.93924, 60.16964]},
    "source": "FMI:urban::observations::airquality::hourly::multipointcoverage",
    "reliability": 1.0,
    # "PM2.5": 6.3,
    # "PM10": 20.8,
    # "SO2": 1.0,
    # "NO2": 35.9,
    # "NO": 10.2,
    # "O3": 1.0,
    "dateObservedFrom": "2023-06-12T08:00:00+00:00",
    "dateObservedTo": "2023-06-12T09:00:00+00:00",
}


def extract_latest_measurements(station_name: str, station_meta: dict, data: dict):
    times = data["times"]
    latest_time = max(times)
    latest_measurements = {}

    for key, value in data.items():
        if key != "times":
            measurement = {"unit": value["unit"], "value": value["values"][times.index(latest_time)]}
            latest_measurements[key] = measurement
    latest_measurements["time"] = latest_time.replace(tzinfo=datetime.timezone.utc)
    result = {station_name: latest_measurements}
    return result


def create_post_data(station_name: str, station_meta: dict, data: dict):
    meta = station_meta[station_name]
    # Create a copy of the template using copy.deepcopy
    p = copy.deepcopy(post_template)
    # Update the id
    p["id"] = f"fmi-{meta[2]}"
    # Update the address
    p["address"]["streetAddress"] = meta[1].split(" ")[1]
    # Update the location
    p["location"]["coordinates"] = meta[5], meta[4]
    p["dateObservedFrom"] = p["dateObservedTo"] = data.pop("time").strftime("%Y-%m-%dT%H:%M:%SZ")

    for k in data.keys():
        p[k] = data[k]["value"]
    print(p["address"]["streetAddress"])
    return p


def post_data(p: dict):
    body = json.dumps(p, indent=2)
    logging.debug(body)
    print(body)
    res = httpx.post(API_URL, json=p, headers=API_HEADERS)
    return res


def main():
    # Pick the 2nd field as key and 3rd field as value of each line using list comprehension to a dict
    aq_stations_dict = {line.split("\t")[1]: line.split("\t") for line in aq_stations.splitlines()}
    print(aq_stations_dict)
    # Pick the 3rd field of each list in aq_stations_dict using list comprehension
    aq_stations_ids = [aq_stations_dict[k][2] for k in aq_stations_dict]
    # Create & separated list of ids like this: fmisid=100662&fmisid=100742
    aq_stations_arg = "&".join([f"fmisid={id}" for id in aq_stations_ids])
    # Create a list of arguments for the query
    now = datetime.datetime.now().astimezone(tz=datetime.timezone.utc).replace(microsecond=0, second=0, minute=0)
    st = (now - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    et = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    args = ["timeseries=True", f"starttime={st}", f"endtime={et}", aq_stations_arg]

    aq = download_stored_query("urban::observations::airquality::hourly::multipointcoverage", args=args)
    # pprint(list(aq.data.keys()))
    # pprint(aq.data)
    for k in aq.data.keys():
        data = extract_latest_measurements(k, aq_stations_dict, aq.data[k])
        p = create_post_data(k, aq_stations_dict, data[k])
        res = post_data(p)
        logging.info(f"Sent {k}, status: {res.status_code} {res.text}")


if __name__ == "__main__":
    main()
