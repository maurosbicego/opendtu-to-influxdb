from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from config import config
from time import sleep
import requests as r
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%Y %H:%M:%S')

client = InfluxDBClient(url=config["influxdb"], token=config["accesstoken"], org=config["org"])
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def assertWatts(value: dict) -> int:
    if value["u"] == "kW" or value["u"] == "kWh":
        return float(value["v"]*1000)
    else:
        return float(value["v"])
    

while True:
    datapoints = []
    try:
        res = r.get("http://{}/api/livedata/status".format(config["opendtuip"])).json()

        p = Point("total").field("power", assertWatts(res["total"]["Power"])).field("yieldDay", assertWatts(res["total"]["YieldDay"])).field("yieldTotal", assertWatts(res["total"]["YieldTotal"]))
        logging.info("Datapoint total: "+str(p))
        datapoints.append(p)
        for inverter in res["inverters"]:
            invRes = r.get("http://{}/api/livedata/status?inv={}".format(config["opendtuip"], inverter["serial"])).json()["inverters"][0]
            gridPoint = Point("grid").tag("inverter", inverter["serial"]).field("output", assertWatts(invRes["AC"]["0"]["Power"])).field("voltage", float(invRes["AC"]["0"]["Voltage"]["v"])).field("current", float(invRes["AC"]["0"]["Current"]["v"])).field("frequency", float(invRes["AC"]["0"]["Frequency"]["v"])).field("reactivePower", float(invRes["AC"]["0"]["ReactivePower"]["v"]))
            logging.info("Datapoint grid from inverter: "+str(gridPoint))
            datapoints.append(gridPoint)
            inverterPoint = Point("inverter").tag("inverter", inverter["serial"]).field("powerDC", assertWatts(invRes["INV"]["0"]["Power DC"])).field("yieldDay", assertWatts(invRes["INV"]["0"]["YieldDay"])).field("yieldTotal", assertWatts(invRes["INV"]["0"]["YieldTotal"])).field("temperature", float(invRes["INV"]["0"]["Temperature"]["v"])).field("efficiency", float(invRes["INV"]["0"]["Efficiency"]["v"]))
            logging.info("Datapoint inverter data: "+str(inverterPoint))
            datapoints.append(inverterPoint)

    except Exception as e:
        logging.error("Error reading data from OpenDTU at http://{}/report".format(config["opendtuip"]))
        logging.error(e)

    try:
        logging.info("Fetched data from OpenDTU. {} datapoints".format(len(datapoints)))
        for point in datapoints:
            write_api.write(bucket=config["bucket"], record=point)
        logging.info("Wrote datapoints")

    except Exception as e:
        logging.error("Error sending data to Influx")
        logging.error(e)
    
    sleep(config["interval"])
    