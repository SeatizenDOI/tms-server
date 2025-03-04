<p align="center">
  <a href="https://github.com/SeatizenDOI/tms-server/graphs/contributors"><img src="https://img.shields.io/github/contributors/SeatizenDOI/tms-server" alt="GitHub contributors"></a>
  <a href="https://github.com/SeatizenDOI/tms-server/network/members"><img src="https://img.shields.io/github/forks/SeatizenDOI/tms-server" alt="GitHub forks"></a>
  <a href="https://github.com/SeatizenDOI/tms-server/issues"><img src="https://img.shields.io/github/issues/SeatizenDOI/tms-server" alt="GitHub issues"></a>
  <a href="https://github.com/SeatizenDOI/tms-server/blob/master/LICENSE"><img src="https://img.shields.io/github/license/SeatizenDOI/tms-server" alt="License"></a>
  <a href="https://github.com/SeatizenDOI/tms-server/pulls"><img src="https://img.shields.io/github/issues-pr/SeatizenDOI/tms-server" alt="GitHub pull requests"></a>
  <a href="https://github.com/SeatizenDOI/tms-server/stargazers"><img src="https://img.shields.io/github/stars/SeatizenDOI/tms-server" alt="GitHub stars"></a>
  <a href="https://github.com/SeatizenDOI/tms-server/watchers"><img src="https://img.shields.io/github/watchers/SeatizenDOI/tms-server" alt="GitHub watchers"></a>
</p>

<div align="center">

# TMS Server

</div>

## Summary

* [Docker](#docker)
* [Installation](#installation)
* [Configure access with QGIS](#configure-access-with-qgis)
* [Seatizen Monitoring](#seatizenmonitoring)
* [Create your dataset](#create-your-dataset)
* [Contributing](#contributing)
* [License](#license)

## Docker

Image are automatically built with a CI pipeline on github. They are available under the name :
* seatizendoi/tms-server:latest

If you want to run docker image from dockerhub add seatizendoi/ to the beginning of image name.

This image docker is a flask server.

Build command :
```bash
docker build -f Dockerfile -t seatizendoi/tms-server:latest .
```

Run command
```bash
docker run --rm -v /home/debian/villien/tiles/:/app/tiles --name tms-server -p 5004:5004 seatizendoi/tms-server:latest
```

## Installation

To ensure a consistent environment for all users, this project uses a Conda environment defined in a `tms_env.yml` file. Follow these steps to set up your environment:

1. **Install Conda:** If you do not have Conda installed, download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

2. **Create the Conda Environment:** Navigate to the root of the project directory and run the following command to create a new environment from the `tms_env.yml` file:
   ```bash
   conda env create -f tms_env.yml
   ```

3. **Activate the Environment:** Once the environment is created, activate it using:
   ```bash
   conda activate tms_env
   ```

## Configure access with QGIS

1. **Load a base map:** Load a base map like Google Satellite available in QuickMapServices in contributors ressources.

2. **Use XYZ Data Connexion:** Open XYZ data connexion and click on new connexion. Filled the popup like this :

* Name: Drone Ifremer DOI
* URL: https://tmsserver.ifremer.re/wmts?request=GetTile&tilematrix={z}&tilerow={x}&tilecol={y}
* Min Zoom level: 5
* Max Zoom level: 26
* Tile resolution: 256*256

<div align="center">
  <img src="assets/qgis.png" alt="Qgis">
</div>

Finally click on `OK`.

You will see the orthophoto tiles on reunion island in the west coast.

## Seatizen Monitoring

You can also visualize the tiles on the map of [seatizenmonitoring](http://seatizenmonitoring.ifremer.re)


## Create your ortho dataset

### 1. Split each orthophoto in tiles


In a first time, you need to gather your tif in one folder (Ex: /path/to/my/folder).

At the root of the folder, create a file called `apply_gdaltiles.sh` (EX: /path/to/my/folder/apply_gdaltiles.sh) and write inside :

```bash
#!/bin/bash

PATTERN=202311
NB_SESSION=$(ls -l | grep ${PATTERN} | wc -l)

for i in $(seq 1 $NB_SESSION); do

  A=$(ls -v | grep ${PATTERN} | sed -n "${i}p")
  gdal2tiles -z 10-22 --processes=12 ${A} tiles_${A}

done
```

Replace the value of `PATTERN` as you wish.

Execute `chmod a+x apply_gdaltiles.sh`

Now, we need to execute the script, so execute this command : 

`docker run --rm --user 1000:1000 -v /path/to/my/folder/:/app -it ghcr.io/osgeo/gdal`

Then inside the docker terminal, write : `cd /app && ./apply_gdaltiles.sh`


### 2. Build the big dataset.

To build the big dataset, we have two approch.

* The first one is to build a global dataset from session tiles.

You need to execute the script `merge_tiles.py` in utils folder like :

`python merge_tiles.py -p /path/to/my/folder`

A global folder will be create in your folder. 

* The second approch is to merge two global folder.

You need to execute the script `big_merge.py` in utils folder like :

`python big_merge.py -pi /path/to/my/folder/where/are/all/global/folder -po /path/folder/out`

## Create your bathy dataset.

Gather all your bathy in one folder.

Use raster.ipynb to create group of bathy file.

Launch gdal with : `docker run --rm -it --user 1000:1000 -v /home/bioeos/Documents/project_hub/tms-server/bathy:/app ghcr.io/osgeo/gdal:latest`

and then go into /app and run `./apply_gdal.sh`

Go into utils/ and run `python merge_tiles.py -p /home/bioeos/Documents/project_hub/tms-server/bathy/tiles/`

Congrats you have a global folder with all your bathy tiles.

## Contributing

Contributions are welcome! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push your branch and submit a pull request.

## License

This framework is distributed under the CC0-1.0 license. See `LICENSE` for more information.
