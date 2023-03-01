# UrbanageGCI - Source data format

The required source data is a set of GeoJSON feature collections, that are to be made available over https. A set of example files are available for reference from Leuven.

The files are available in the [samples](samples/) folder.

## Point data (amenities)

* Trees ([leuven-tree.json](samples/leuven-tree.json))
* Benches ([leuven-bench.json](samples/leuven-bench.json))
* Drinking water fountains ([leuven-drinking_water.json](samples/leuven-drinking_water.json))
* Toilets ([leuven-toilet.json](samples/leuven-toilet.json))

## Park polygons

Park polygons (including walkable and green areas, excluding heavily trafficed areas not friendly for pedestrians, such as cycle paths) ([leuven-park.json](samples/leuven-park.json))

## Calculation boundaries

Polygonal area limit for processing ([leuven-public-area.json](samples/leuven-public-area.json))

## Heat stress

A single channel TIF raster for depicting the heat stress, that affects the GCI negatively. ([Sample as ZIP](leuven-threshold-heat-stress-min-and-max.zip))

A following palette is used:

0. Undefined 
1. Heat stress level 1
2. Heat stress level 2
3. Heat stress level 3
4. Heat stress level 4
5. Heat stress level 5
