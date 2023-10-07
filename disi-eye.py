import reader
import detector
import printer
import threading
import json

# Leer archico de configuracion
configFile=open("config.json", "r")
webcamServers=json.load(configFile)
configFile.close()
# Variables 
frameBuffer={}
frameBufferProcessed={}
frameBufferLock=threading.Lock()
frameBufferProcessedLock=threading.Lock()

#Connecion con las webcams
reader.createIpCamerasReaders(webcamServers,frameBuffer,frameBufferLock)
#Detector de objetos
detector.createDetecor(frameBuffer,frameBufferProcessed,frameBufferLock,frameBufferProcessedLock)
#Mostrar detecciones
printer.createPrinter(frameBufferProcessed,frameBufferProcessedLock)
