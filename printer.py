import cv2 as cv
import threading

def printImageThread(frameBufferProcessed,frameBufferProcessedLock):

   while True:
    frameBufferProcessedLock.acquire()
    auxFrameBuffer=frameBufferProcessed.copy()
    frameBufferProcessedLock.release()
    if not(auxFrameBuffer=={}):
      for frame in auxFrameBuffer.keys():
        image=auxFrameBuffer.get(frame)
        image = cv.resize(image,(400,250))
        cv.imshow(frame, image)
        cv.waitKey(1)
   cv.destroyAllWindows()

def createPrinter(frameBufferProcessed,frameBufferProcessedLock):
  thread=threading.Thread(target=printImageThread,args=(frameBufferProcessed,frameBufferProcessedLock))
  thread.start()