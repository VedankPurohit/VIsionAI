import streamlit as st
import cv2
import numpy as np
import tempfile

#import sys; print(sys.executable)


cap = cv2.VideoCapture(1)

st.title("Video Feed")

PlaceHolderFrame = st.empty()

StopButton = st.button("Stop")

while cap.isOpened() and not StopButton:
    ret, frame = cap.read()
    if not ret:
        st.write("Error: Unable to capture video feed")
        break
    
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame = cv2.flip(frame, -1)
    #frame = cv2.resize(frame, (640, 480))
    PlaceHolderFrame.image(frame, channels="RGB")

    if cv2.waitKey(1) & 0xFF == ord("q") or StopButton:
        break

cap.release()
cv2.destroyAllWindows()