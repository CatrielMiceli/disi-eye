import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#def influxdbConnectDISILAB():
#   token = "TlovmbFuFg-B23L9qhVAJcMZN6o2sUg6Hj5ATCALXZOtc9Rnfrs6pE15ukE7bTSuJ1ebqO1UI0m0zRFBejw0fw=="
#   org = "sed"
#   url = "http://localhost:8086"
#   write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
#   return  write_client

def influxdbConnectDISILABFromFile():
   #client = InfluxDBClient.from_config_file(f'{os.path.dirname(__file__)}/config.ini')
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
         #print(object+ ': ' + str(listObjectDetected.count(object))+" ",end="")
      #print(stringQuery)s
      point = (stringQuery)
      #write_api.write(bucket=bucket, org="sed", record=point)
      write_api.write(bucket=bucket, record=point)  