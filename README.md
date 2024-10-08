# TMS Server

[TOC]

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

* Name: "Drone Ifremer DOI"
* URL: "http://127.0.0.1:5000/wmts?request=GetTile&tilematrix={z}&tilerow={x}&tilecol={y}
* Min Zoom level: 5
* Max Zoom level: 23
* Tile resolution: 256*256

<!-- TODO Screenshot -->

Finally click on `OK`.

You will see the orthophoto tiles on reunion island in the west coast.

## Seatizenmonitoring

You can also visualize the tiles on the map of [seatizenmonitoring](http://seatizenmonitoring.ifremer.re)