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

    model = YOLO("Vision AI/Models/yolov8n.pt")

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

        filtered_labels = []
        filtered_detections = []

        for bbox, confidence, class_id, _ in detections:
            label = model.model.names[class_id]
            # Filter out the person label and its bounding box
            if label != "person":
                filtered_labels.append({"label": label, "confidence": float(confidence)})
                filtered_detections.append((bbox, confidence, class_id))

        annotated_frame = BoxAnnotator.annotate(
            scene=frame,
            detections=filtered_detections,
            labels=[f"{label['label']} {label['confidence']:0.8f}" for label in filtered_labels]
        )
        
        frame_data = {"objects": filtered_labels}

        cv2.imshow("video", annotated_frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
