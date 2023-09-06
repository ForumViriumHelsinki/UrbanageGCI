import copy
import json
import logging
import sys

import httpx

# Set logging level to DEBUG to see debug messages
logging.basicConfig(level=logging.INFO)

API_URL = sys.argv[1]
API_HEADERS = {
    "Content-Type": "application/json",
    "Fiware-Service": "helsinki",
    "User-Agent": "UrbanAge uiras2api/0.0.1",
}

wt_template = {
  "dateObserved": "2023-07-06T08:00:00Z",
  "dev_id": "1",
  "id": "0",
  "location": {
    "coordinates": [
      "24.9506",
      "60.18739"
    ],
    "type": "Point"
  },
  "temperature": 24.9,
  "type": "WaterObserved"
}

def convert_geojson_to_dict(geojson: dict) -> list:
    # Translate this to english:
    # Muuntaa geojson-tiedoston jokaisen FeatureCollectionin Featuren haluttuun muotoon

    """Convert geojson object's FeatureCollections to FiWare format

    Args:
      geojson: Geojson object.

    Returns:
      List of dictionaries in FiWare format.
    """
    features = geojson["features"]
    new_wt = []
    for feature in features:
        new = copy.deepcopy(wt_template)
        new["dev_id"] = feature["id"]
        new["temperature"] = feature["properties"]["temp_water"]
        new["dateObserved"] = feature["properties"]["time"]
        # new["dateObserved"] = "2023-09-06T08:44:21Z"  # testing if this works better than +00:00 notation
        new["location"] = feature["geometry"]
        # Convert coordinates to string
        # new["location"]["coordinates"] = [str(x) for x in new["location"]["coordinates"]]  # testing if this works?
        new_wt.append(new)
    return new_wt


def post_data(p: dict):
    body = json.dumps(p, indent=2)
    logging.debug(body)
    # print(body)
    res = httpx.post(API_URL, json=p, headers=API_HEADERS)
    return res


def main():
    # Get uiras data from url using httpx
    url = "https://iot.fvh.fi/opendata/uiras/uiras2_v2.geojson"
    # Convert geojson to dict
    uiras = httpx.get(url).json()
    wt_list = convert_geojson_to_dict(uiras)
    for u in wt_list:
        res = post_data(u)
        logging.info(f"Sent {u}, status: {res.status_code} {res.text}")
        exit()


if __name__ == "__main__":
    main()
