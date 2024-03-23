# OpenDTU-to-InfluxDB
Tool to periodically send the data from OpenDTU to a Influx bucket. Tested with OpenDTU v24.3.15 and with a Hoymiles HM-600 inverter.

-> Kleines Tool/Script zum Senden von Daten aus OpenDTU in ein InfluxDB-Bucket

## Usage
This tool can be used with *docker-compose*. It can also be run directly

### Configuration
First, copy the file `sample-config.py` to `config.py` and adapt all the necessary details. You need to create an API Key in Influx and adapt the config according to your setup.

**If** you have setup InfluxDB with *https* place the root CA certificate that corresponds to the InfluxDB instance to `root.crt`. It will be installed inside the Docker container.

If your instance has a DNS name that is not resolvable in the docker container, add it to the `docker-compose.yml`

Everything should now be configured

### Running with docker-compose
**Note:** It is assumed that docker and docker-compose are already installed
Copy everything to the place of your choice, then, you can start it:
`sudo docker-compose up -d`

If you make any changes, you need to rebuild the Docker by using `sudo docker-compose up -d --build`



# Disclaimer / In case of problems
Use at own risk.
I created this tool for my own use, and it is very basic and can contain a lot of errors, also depending on the installation.
I might add more functionality if people are interested. Feel free to open an issue in case of requests or errors.