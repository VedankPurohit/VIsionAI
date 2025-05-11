import cv2

def crop_main_object(image_location, save_dir):
  """
  This function attempts to crop the main object in an image and saves it.

  Args:
      image_location: Path to the image file.
      save_dir: Path to save the cropped image.
  """
  # Read the image
  image = cv2.imread(image_location)

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  largest_area = 0
  largest_contour_index = None
  for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area > largest_area:
      largest_area = area
      largest_contour_index = i

  if largest_contour_index is None:
    print("No significant object found in the image.")
    return

  x, y, w, h = cv2.boundingRect(contours[largest_contour_index])

  cropped_image = image[y:y+h, x:x+w]

  cv2.imwrite(save_dir, cropped_image)

if __name__ == "__main__":
    image_location = r"Vision AI\Tests\Realme 11 Pro plus in_11.jpeg"
    save_dir = "Vision AI\Results\FocusObject.jpg"
    crop_main_object(image_location, save_dir)
