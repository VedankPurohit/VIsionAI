import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
import tempfile

width , height = 640, 640
cap = cv2.VideoCapture(1)
model = YOLO("Models\ImgPredict.pt")

BoxAnnotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness= 2,
    text_scale=1
)

import streamlit as st #here is it

st.title("Video Feed")

PlaceHolderFrame = st.empty()

StopButton = st.button("Stop")
ProcessButton = st.button("Process")


while cap.isOpened() and not StopButton:
    res, frame = cap.read()
    if not res:
        st.write("Error: Unable to capture video feed")
        break

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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame = cv2.flip(frame, -1)
    #frame = cv2.resize(frame, (640, 480))
    PlaceHolderFrame.image(frame, channels="RGB")
    
    if cv2.waitKey(1) & 0xFF == ord("q") or StopButton:
        break
cap.release()
cv2.destroyAllWindows()
