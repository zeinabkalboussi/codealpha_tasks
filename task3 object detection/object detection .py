import cv2
import numpy as np


net = cv2.dnn.readNetFromDarknet('C:/Users/Zeinab Kalboussi/Downloads/yolov4.cfg', 'C:/Users/Zeinab Kalboussi/Downloads/yolov4.weights')
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

DEFAULT_CONFIDENCE = 0.5
THRESHOLD = 0.4

with open('C:/Users/Zeinab Kalboussi/Downloads/coco.names', 'r') as f:
    LABELS = f.read().strip().split('\n')


video_path = 'C:/Users/Zeinab Kalboussi/Downloads/Sadio mané le triplé le plus rapide au monde.mp4'  
cap = cv2.VideoCapture(video_path)

while True:
    ret, image = cap.read()
    if not ret:
        break
    
    height, width, _ = image.shape

    blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    
    for output in layerOutputs:
     
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > DEFAULT_CONFIDENCE:
                box = detection[0:4] * np.array([width, height, width, height])
                (centerX, centerY, W, H) = box.astype("int")
                x = int(centerX - (W / 2))
                y = int(centerY - (H / 2))
                boxes.append([x, y, int(W), int(H)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, DEFAULT_CONFIDENCE, THRESHOLD)

    COLORS = np.random.uniform(0, 255, size=(len(boxes), 3))

    if len(indexes) > 0:
        for i in indexes.flatten():
            (x, y, w, h) = boxes[i]
            color = COLORS[i]
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, text, (x, y + 20), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    cv2.imshow('Video', image)
    if cv2.waitKey(1000) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
