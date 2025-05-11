from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2
import os

model = YOLO("Vision AI/Models/yolov8l.pt")
names = model.names

image_path = "Vision AI/Tests/Realme 11 Pro plus in_11.jpeg"
assert os.path.isfile(image_path), "Image file not found"

crop_dir_name = "Vision AI\Results"
if not os.path.exists(crop_dir_name):
    os.mkdir(crop_dir_name)

im0 = cv2.imread(image_path)
assert im0 is not None, f"Unable to read image: {image_path}"

results = model.predict(im0, show=False)
boxes = results[0].boxes.xyxy.cpu().tolist()
clss = results[0].boxes.cls.cpu().tolist()
annotator = Annotator(im0, line_width=2, example=names)
idx = 0
if boxes is not None:
    for box, cls in zip(boxes, clss):
        idx += 1
        print(f"Detected object {idx} with class: {names[int(cls)]}")
        annotator.box_label(box, color=colors(int(cls), True), label=names[int(cls)])
        crop_obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        crop_filename = os.path.join(crop_dir_name, f"{idx}.png")
        print(f"Saving cropped object {idx} to: {crop_filename}")
        cv2.imwrite(crop_filename, crop_obj)