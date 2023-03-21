# UrbanageGCI - Running the computation

The computation is run on server by issuing a POST request, where the prepared GeoJSON URLs are given as parameters.

> curl --location 'https://api.dev.urbanage.odt.imec-apt.be/ur-api-rest-gcm/green-comfort-score' \
--header 'Content-Type: application/json' \
--data '{
    "bench": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-bench.json",
    "calculationArea": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-public-area.json",
    "drinkingWater": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-drinking_water.json",
    "h3Resolution": 12,
    "heatScoreTif": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-threshold-heat-stress-min-and-max.tif",
    "inputCity": "leuven",
    "park": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-park.json",
    "postOutputToUrl": "https://api.dev.urbanage.odt.imec-apt.be/ur-api-rest-gcm/v1/dataset",
    "toilet": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-toilet.json",
    "tree": "https://stcitiespublic.blob.core.windows.net/assets/urbanage/green-comfort-model/input/leuven/leuven-tree.json"
}'

For the Helsinki data, the CURL command is as follows:
> curl --location 'https://gcm.dev.ecosystem-urbanage.eu/v1/green-comfort-score' \
--header 'Content-Type: application/json' \
--data '{
    "h3Resolution": 12,
    "inputCity": "Helsinki",
    "calculationArea": "https://proto.fvh.io/urbanage/HelsinkiPublicArea_2.json",
    "bench": "https://proto.fvh.io/urbanage/HelsinkiBenches.json",
    "drinkingWater": "https://proto.fvh.io/urbanage/HelsinkiDrinkingWater.json",
    "park": "https://proto.fvh.io/urbanage/HelsinkiParks.json",
    "toilet": "https://proto.fvh.io/urbanage/HelsinkiToilets.json",
    "tree": "https://proto.fvh.io/urbanage/HelsinkiTrees.json",
    "heatScoreTif": "",
    "postOutputToUrl": "http://ur-api-rest-gcm:9000/v1/dataset",
    "statusUrl": "http://ur-api-rest-gcm:9000/v1/status"
}'

The progress can be monitored at:
> https://airflow.dev.ecosystem-urbanage.eu/dagrun/list/?_flt_3_dag_id=run-ur-model-green-comfort