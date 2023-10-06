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
frameBufferProcesed={}
frameBufferLock=threading.Lock()
frameBufferProcesedLock=threading.Lock()

#Connecion con las webcams
reader.createIpCamerasReaders(webcamServers,frameBuffer,frameBufferLock)
#Detector
detector.createDetecor(frameBuffer,frameBufferProcesed,frameBufferLock,frameBufferProcesedLock)
#Mostrar detecciones
printer.createPrinter(frameBufferProcesed,frameBufferProcesedLock)
