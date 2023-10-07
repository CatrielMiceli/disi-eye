import cv2 as cv
import time
import bdconnect as bd
import threading

def getDNNabels91():
   cocoLabels=["person", "bicycle","car","motorcycle","airplane",
               "bus","train","truck","boat","traffic light","fire hydrant",
               "street sign","stop sign","parking meter","bench","bird","cat",
               "dog","horse","sheep","cow","elephant","bear",
               "zebra","giraffe","hat","backpack","umbrella","shoe",
               "eye glasses","handbag","tie","suitcase","frisbee","skis",
               "snowboard","sports ball","kite","baseball bat","baseball glove","skateboard",
               "surfboard","tennis racket","bottle","plate","wine glass","cup",
               "fork","knife","spoon","bowl","banana","apple",
               "sandwich","orange","broccoli","carrot","hot dog","pizza",
               "donut","cake","chair","couch","potted plant","bed",
               "mirror","dining table","window","desk","toilet","door",
               "tv","laptop","mouse","remote","keyboard","cell phone",
               "microwave","oven","toaster","sink","refrigerator","blender",
               "book","clock","vase","scissors","teddy bear","hair drier",
               "toothbrush","hair brush"]
   return cocoLabels

def setBoundingColor(label):
   greenLabel= ["person"]
   blueLabel= ["tv","laptop"]
   redLabel=[  "bottle","plate","wine glass","cup",
               "fork","knife","spoon","bowl","banana","apple",
               "sandwich","orange","broccoli","carrot","hot dog","pizza",
               "donut","cake","vase"]
   if label in greenLabel:
      return (0,255,0) #green
   elif label in redLabel:
      return (0,0,255) #red
   elif label in blueLabel:
      return (255,0,0) #blue
   else:
      return (0,180,180) #yellow
   
def getNumberPerLebelTerminalLog(listObjectDetected,time,desc):
   
   if len(listObjectDetected)>0:
      print("LOG: "+ str(time) +" "+desc+" totalObjects: "+ str(len(listObjectDetected))+" - ",end="")
      typeObject=set(listObjectDetected)
      for object in typeObject:
         print(object+ ': ' + str(listObjectDetected.count(object))+" ",end="")
      print("")

def detectObjectTread(frameBuffer,frameBufferProcessed,frameBufferLock,frameBufferProcessedLock):
   labels = getDNNabels91()
   connectInfluxDB = bd.influxdbConnectDISILABFromFile()
   model = 'frozen_inference_graph.pb'
   config = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
   objectDetector= cv.dnn.readNetFromTensorflow(model=model, config=config)
   while True:
      frameBufferLock.acquire()
      auxFrameBuffer=frameBuffer.copy()
      frameBufferLock.release()
      if not(auxFrameBuffer=={}):
        for frame in auxFrameBuffer.keys():
         image=auxFrameBuffer.get(frame)
         image_height, image_width, _ = image.shape
         blob = cv.dnn.blobFromImage(image=image,scalefactor=(1.0 / 127.5), size=(320, 320), mean=(127.5, 127.5, 127.5), swapRB=True)
         objectDetector.setInput(blob)
         output = objectDetector.forward()
         objectDetected = []  
         for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > .6:
               class_id = detection[1]
               class_name = labels[int(class_id)-1]
               box_x = detection[3] * image_width
               box_y = detection[4] * image_height
               box_width = detection[5] * image_width
               box_height = detection[6] * image_height
               color=setBoundingColor(class_name)
               cv.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
               (w, h), _ = cv.getTextSize(class_name +" "+ str(int(100*confidence)), cv.FONT_HERSHEY_SIMPLEX, 1, 1)
               image = cv.rectangle(image, (int(box_x), int(box_y - 5)),((int(box_x+w), int((box_y-5)-h))), color, -1)
               textColor=(255,255,255)
               cv.putText(image, class_name +" "+ str(int(100*confidence)), (int(box_x), int(box_y - 5)), cv.FONT_HERSHEY_SIMPLEX, 1, textColor, 2)
               objectDetected.append(class_name)
         frameBufferProcessedLock.acquire()
         frameBufferProcessed[frame]=image
         frameBufferProcessedLock.release()
         bd.getNumberPerLebelInfluxdb(connectInfluxDB,objectDetected ,frame)
      auxFrameBuffer={}

def createDetecor(frameBuffer,frameBufferProcessed,frameBufferLock,frameBufferProcessedLock):
   thread=threading.Thread(target=detectObjectTread,args=(frameBuffer,frameBufferProcessed,frameBufferLock,frameBufferProcessedLock))
   thread.start()