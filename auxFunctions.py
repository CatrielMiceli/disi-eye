
# Lista de objetos detectables
def getListDetectableObjects():
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

# Contador de total de objetos y objetos por etiqueta que los imprime por la terminal
def getNumberPerLebelTerminalLog(listObjectDetected,time):
   
   if len(listObjectDetected)>0:
      print("LOG: "+ str(time) +" totalObjects: "+ str(len(listObjectDetected))+" - ",end="")
      typeObject=set(listObjectDetected)
      for object in typeObject:
         print(object+ ': ' + str(listObjectDetected.count(object))+" ",end="")
      print("")
   
# Selecciona el color segun el objeto
def setColorBounding(label):
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