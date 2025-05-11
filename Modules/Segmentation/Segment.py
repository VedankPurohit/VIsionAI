import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import json


def main():
    width , height = 640, 640
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("http://100.64.255.175:8080/video")
    #cap.set(3,1024) # set Width
    #cap.set(4,1024) # set Height

    model = YOLO("Vision AI/Models/yolov8l.pt")

    BoxAnnotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness= 2,
        text_scale=1
    )

    data = []

    while True:
        res, frame = cap.read()

        result = model(frame)[0]
        detections = sv.Detections.from_yolov8(result)

        labels = [
            {"label": model.model.names[class_id], "confidence": float(confidence)}
            for _, confidence, class_id, _ in detections
        ]
        print(labels)
        
        annotated_frame = BoxAnnotator.annotate(
            scene=frame,
            detections=detections,
            labels=[f"{label['label']} {label['confidence']:0.8f}" for label in labels]
        )
        
        frame_data = { "objects": labels}
        #print(frame_data)

        cv2.imshow("video", annotated_frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
