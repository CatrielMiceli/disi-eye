import cv2 as cv
import time
import threading

def IpCameraReaderThread(urlCamera,name,frameBuffer,frameBufferLock):
   cap = cv.VideoCapture(urlCamera)
   while cap.isOpened():
      ret, frame = cap.read()
      if ret == True:
         frameBufferLock.acquire()
         frameBuffer[name]=frame
         frameBufferLock.release()
      else:
         frameBufferLock.acquire()
         if name in frameBuffer:
           del(frameBuffer[name])
         frameBufferLock.release()
         cap.release()
         cap = cv.VideoCapture(urlCamera)
   cap.release()
   time.sleep(1)
   IpCameraReaderThread(urlCamera,name,frameBuffer,frameBufferLock)


def createIpCamerasReaders(webcamServers,frameBuffer,frameBufferLock):
 for webcam in webcamServers[:]:
  dirConnection=webcam.get("rtsp-dir")
  desc=webcam.get("desc")
  print(dirConnection)
  print(desc)
  thread=threading.Thread(target=IpCameraReaderThread,args=(dirConnection,desc,frameBuffer,frameBufferLock),name=desc)
  thread.start()