import cv2

# Open a connection to the webcam (default webcam is usually at index 0)


def CaptureSingleFrame(cap):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        return None
    
    return frame

if __name__ == "__main__":    
    cap = cv2.VideoCapture(0)


    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    # Release the capture and close the windows
    cap.release()
    cv2.destroyAllWindows()
