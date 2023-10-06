import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



def influxdbConnectDISILABFromFile():
   client = InfluxDBClient.from_config_file("bdconfig.ini")
   return client

def getNumberPerLebelInfluxdb(connect,listObjectDetected, place):   
   if len(listObjectDetected)>0:
      bucket="disi-lab"
      write_api = connect.write_api(write_options=SYNCHRONOUS)
      stringQuery= Point("objetosLab").tag("Laboratorio",place)
      typeObject=set(listObjectDetected)
      for object in typeObject:
         stringQuery= stringQuery.field(object,(listObjectDetected.count(object)))
      point = (stringQuery)
      write_api.write(bucket=bucket, record=point)  