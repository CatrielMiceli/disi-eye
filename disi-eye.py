import auxFunctions as af
import cv2 as cv
import time


#Colocar la direccion de la ipcam en el archivo rtsp-config.txt
rtspFile = open('rtsp-config.txt')
line = rtspFile.readline()

# Objetos que detecta red
labels = af.getListDetectableObjects()
  
# Cargamos la red neuronal
model = 'frozen_inference_graph.pb'
config = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
model = cv.dnn.readNetFromTensorflow(model=model, config=config)

cap = cv.VideoCapture(line)

while cap.isOpened():
   ret, frame = cap.read()
   if ret:
       image = frame
       image_height, image_width, _ = image.shape
       # Cargamos la imagen en la red neuronal
       blob = cv.dnn.blobFromImage(image=image,scalefactor=(1.0 / 127.5), size=(320, 320), mean=(127.5, 127.5, 127.5), swapRB=True)
       # Empezamos a contar el tiempo para calcular los FPS
       start = time.time()
       # Mandamos la imagen para procesar las detecciones
       model.setInput(blob)
       output = model.forward()       
       objectDetected = []
       # Analizamos las detecciones
       for detection in output[0, 0, :, :]:
           # Leemos el valor de confianza de la deteccion
           confidence = detection[2]
           # Elejimos el umbral de confianza de la deteccion
           if confidence > .6:
               # Averiguamos el tipo de objeto
               class_id = detection[1]
               class_name = labels[int(class_id)-1]
               # Obtenemos las coordenadas el recangulo delimitador
               box_x = detection[3] * image_width
               box_y = detection[4] * image_height
               box_width = detection[5] * image_width
               box_height = detection[6] * image_height
               # Dibujamos la pantalla
               color=af.setColorBounding(class_name)
               cv.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), color, thickness=2)
               (w, h), _ = cv.getTextSize(class_name +" "+ str(int(100*confidence)), cv.FONT_HERSHEY_SIMPLEX, 1, 1)
               image = cv.rectangle(image, (int(box_x), int(box_y - 5)),((int(box_x+w), int((box_y-5)-h))), color, -1)
               textColor=(255,255,255)
               cv.putText(image, class_name +" "+ str(int(100*confidence)), (int(box_x), int(box_y - 5)), cv.FONT_HERSHEY_SIMPLEX, 1, textColor, 2)
               #Agregamos el objeto detectado a la lista de objetos detectados para los logs
               objectDetected.append(class_name)
                           
       # obtenemos el tiempo despues de la deteccion
       end = time.time()
       # Calculamos el fps
       fps = 1 / (end-start)
       # Colocamos el FPS en la pantalla
       cv.putText(image, f"{fps:.2f} FPS", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)
       # transforma el tamaño de la imagen a gusto del consumidor tamaño ancho y alto.
       image = cv.resize(image,(700,500))
       cv.imshow('image', image)
       # Escribimos los logs
       af.getNumberPerLebelTerminalLog(objectDetected,time.ctime())
       # Se corta el pograma apretando la q sobre la transmision
       if cv.waitKey(1) & 0xFF == ord('q'):
           break
   else:
       break
# Liberamos los recursos

rtspFile.close()
cap.release()
cv.destroyAllWindows()