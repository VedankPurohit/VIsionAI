import cv2

def crop_faces(image_location, save_dir):
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier('Modules\Segmentation\haarcascade_frontalface_default.xml')

    # Read the image
    image = cv2.imread(image_location)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Crop and save each face
    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        cv2.imwrite(f"{save_dir}/face_{i+1}.jpg", face)

    print(f"{len(faces)} faces detected and saved.")

if __name__ == "__main__":
    image_location = r"Tests\Realme 11 Pro plus in_11.jpeg"
    save_dir = "Results"
    crop_faces(image_location, save_dir)