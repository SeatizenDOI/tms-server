# How to produce the ortho tiles.


## Create tiles for UAV and ASV orthophoto

Gather all your uav ortho in one folder.

Apply the script `0.apply_tif_gdal_uav.sh` and change the `RASTER_FOLDER` path:
```bash
#!/bin/bash

TILES_FOLDER=/app/output/tiles
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

```

If the script doesn't launch, you can use a docker image like : 

`docker run --rm --user 1000:1000 -v /media/bioeos/E1/drone/drone_ortho_tif/:/app -v ./:/code -it ghcr.io/osgeo/gdal`

But you need to set `RASTER_FOLDER` like `RASTER_FOLDER=/app`



## Merge tiles_folder.

Execute the script `python 2.merge_tiles_folder.py`. 