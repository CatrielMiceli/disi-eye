import cv2 as cv
import threading

def printImageThread(frameBufferProcesed,frameBufferProcesedLock):
   
   while True:
    frameBufferProcesedLock.acquire()
    auxFrameBuffer=frameBufferProcesed.copy()
    frameBufferProcesedLock.release()
    #print(auxFrameBuffer)
    if not(auxFrameBuffer=={}):
      for frame in auxFrameBuffer.keys():
        #print(frame)
        image=auxFrameBuffer.get(frame)
        image = cv.resize(image,(400,250))
        cv.imshow(frame, image)
        cv.waitKey(1)
    #auxFrameBuffer={}
    #time.sleep(0.1)
   cv.destroyAllWindows()

def createPrinter(frameBufferProcesed,frameBufferProcesedLock):
  thread=threading.Thread(target=printImageThread,args=(frameBufferProcesed,frameBufferProcesedLock))
  thread.start()