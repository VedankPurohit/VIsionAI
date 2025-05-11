import cv2
import numpy as np

def ClearestImg(num_captures, delay=1, cap=cv2.VideoCapture(0),image = r"Results\clearest_image.jpg"):

  # Initialize variables
  #cap = cv2.VideoCapture(0)
  clearest_image = None
  clearest_score = -float('inf')

  # Capture loop
  for i in range(num_captures):
    ret, frame = cap.read()
    if not ret:
      print("Error capturing image")
      continue


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    if laplacian > clearest_score:
      clearest_image = frame.copy()
      clearest_score = laplacian

    cv2.imshow('Capturing...', frame)
    cv2.waitKey(1)

    cv2.waitKey(delay) # delay in ms

  cap.release()
  cv2.destroyAllWindows()

  if clearest_image is not None:
    cv2.imwrite(image, clearest_image)
    print("Saved clearest image!")
  else:
    print("No images captured successfully.")

# Example usage
if __name__ == "__main__":
  cap = cv2.VideoCapture(0)

  ClearestImg(10, 500, cap)
