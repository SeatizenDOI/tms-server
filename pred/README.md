# Generate predictions tiles by year


## Convert all your rasters into tiles folder.

```bash

#!/bin/bash

TILES_FOLDER=./output/tiles
rm -rf $TILES_FOLDER
mkdir -p $TILES_FOLDER

COLOR_FOLDER=./output/rasters_color
rm -rf $COLOR_FOLDER
mkdir -p $COLOR_FOLDER

RASTER_FOLDER=/app

for filename in $RASTER_FOLDER/*.tif;
do
    echo $filename;
    BASENAME=$(basename "$filename" .tif)

    if [ ! -f $filename ]; then
        echo "File not found: ${filename}"
        continue
    fi
    COLOR_OUTPUT_FILE="${COLOR_FOLDER}/${BASENAME}_color.tif"

    gdaldem color-relief $filename color.txt $COLOR_OUTPUT_FILE -alpha -co COMPRESS=LZW

    TILE_OUTPUT_FOLDER="${TILES_FOLDER}/tiles_${BASENAME}_color"

    gdal2tiles --processes=12 -x -n -z 10-22 $COLOR_OUTPUT_FILE $TILE_OUTPUT_FOLDER

done

```

If the script doesn't launch, you can use a docker image like : 

`docker run --rm --user 1000:1000 -v /media/bioeos/E/drone/serge_ortho_pred/final_predictions_raster/:/app -v ./:/code -it ghcr.io/osgeo/gdal`

But you need to set `RASTER_FOLDER` like `RASTER_FOLDER=/app`


## Merge tiles_folder.

Execute the script `python 2.merge_tiles_folder.py`. 