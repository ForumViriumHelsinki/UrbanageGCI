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
