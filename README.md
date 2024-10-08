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
* URL: http://ifremer.re:5004/wmts?request=GetTile&tilematrix={z}&tilerow={x}&tilecol={y}
* Min Zoom level: 5
* Max Zoom level: 23
* Tile resolution: 256*256

<div align="center">
  <img src="assets/qgis.png" alt="Qgis">
</div>

Finally click on `OK`.

You will see the orthophoto tiles on reunion island in the west coast.

## Seatizen Monitoring

You can also visualize the tiles on the map of [seatizenmonitoring](http://seatizenmonitoring.ifremer.re)

## Contributing

Contributions are welcome! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push your branch and submit a pull request.

## License

This framework is distributed under the wtfpl license. See `LICENSE` for more information.