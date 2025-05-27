#!/bin/bash

TILES_FOLDER=/app/output/tiles_uav
mkdir -p $TILES_FOLDER

RASTER_FOLDER=/app

for filename in $RASTER_FOLDER/*.tif;
do
    echo $filename;
    BASENAME=$(basename "$filename" .tif)

    if [ ! -f $filename ]; then
        echo "File not found: ${filename}"
        continue
    fi

    TILE_OUTPUT_FOLDER="${TILES_FOLDER}/tiles_${BASENAME}"

    if [[ "$BASENAME" == *UAV* ]]; then
        gdal2tiles --processes=22 --no-kml -e -x -n -z 10-25 $filename $TILE_OUTPUT_FOLDER
    else
        gdal2tiles --processes=22 --no-kml -e -x -n -z 21-28 $filename $TILE_OUTPUT_FOLDER
    fi
done