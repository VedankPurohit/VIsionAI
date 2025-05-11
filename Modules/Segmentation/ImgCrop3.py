from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2
import os
import numpy as np

model = YOLO("Vision AI/Models/yolov8l.pt")
names = model.names

image_path = "Vision AI\Tests\Realme 11 Pro plus in_11.jpeg"
assert os.path.isfile(image_path), "Image file not found"

crop_dir_name = "ultralytics_crop"
if not os.path.exists(crop_dir_name):
    os.mkdir(crop_dir_name)

im0 = cv2.imread(image_path)
assert im0 is not None, f"Unable to read image: {image_path}"

def downscale_image(image, target_size):
    h, w, _ = image.shape
    if h > target_size or w > target_size:
        if h > w:
            new_h = target_size
            new_w = int(w * (target_size / h))
        else:
            new_w = target_size
            new_h = int(h * (target_size / w))
        resized_image = cv2.resize(image, (new_w, new_h))
        return resized_image
    else:
        return image

downscaled_im0 = downscale_image(im0, 640)

results = model.predict(downscaled_im0, show=False)
boxes = results[0].boxes.xyxy.cpu().tolist()
clss = results[0].boxes.cls.cpu().tolist()

annotator = Annotator(downscaled_im0, line_width=2, example=names)

for idx, (box, cls) in enumerate(zip(boxes, clss), start=1):
    label_name = names[int(cls)]
    print(f"Detected object {idx} with class: {label_name}")
    annotator.box_label(box, color=colors(int(cls), True), label=label_name)
    crop_obj = downscale_image(im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])], 640)
    crop_filename = os.path.join(crop_dir_name, f"{label_name}_{idx}.png")
    print(f"Saving cropped object {idx} with label {label_name} to: {crop_filename}")
    cv2.imwrite(crop_filename, crop_obj)
