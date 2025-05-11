import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np


def Feed():
    width , height = 640, 640
    cap = cv2.VideoCapture(1)
    model = YOLO("Models\ImgPredict.pt")

    BoxAnnotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness= 2,
        text_scale=1
    )

    while True:
        res, frame = cap.read()

        result = model(frame)[0]
        detectons = sv.Detections.from_yolov8(result)

        labels = [
            f"{model.model.names[class_id]} {confidence:0.8f}"
            for _, confidence, class_id, _ in detectons
        ]
        frame = BoxAnnotator.annotate(
            scene=frame,
            detections=detectons,
            labels=labels
        )

        cv2.imshow("video", frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Feed()
    