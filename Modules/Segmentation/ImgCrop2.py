from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2
import os
import numpy as np

model = YOLO("Vision AI/Models/yolov8l.pt")
names = model.names

image_path = "Vision AI/Results/1ImageDownScale.png"
assert os.path.isfile(image_path), "Image file not found"

crop_dir_name = "Vision AI\Results"
if not os.path.exists(crop_dir_name):
    os.mkdir(crop_dir_name)

im0 = cv2.imread(image_path)
assert im0 is not None, f"Unable to read image: {image_path}"

# Divide the image into patches if it's larger than 640x640
h, w, _ = im0.shape
patch_size = 640
if h > patch_size or w > patch_size:
    patches = []
    for y in range(0, h, patch_size):
        for x in range(0, w, patch_size):
            patch = im0[y:y+patch_size, x:x+patch_size]
            patches.append(patch)
else:
    patches = [im0]

for patch_idx, patch in enumerate(patches, start=1):
    print(f"Processing patch {patch_idx}/{len(patches)}")

    results = model.predict(patch, show=False)
    boxes = results[0].boxes.xyxy.cpu().tolist()
    clss = results[0].boxes.cls.cpu().tolist()

    # Convert patch to contiguous array
    patch = np.ascontiguousarray(patch)

    annotator = Annotator(patch, line_width=2, example=names)

    for idx, (box, cls) in enumerate(zip(boxes, clss), start=1):
        label_name = names[int(cls)]
        print(f"Detected object {idx} with class: {label_name}")
        annotator.box_label(box, color=colors(int(cls), True), label=label_name)
        crop_obj = patch[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        crop_filename = os.path.join(crop_dir_name, f"{label_name}_{patch_idx}_{idx}.png")
        print(f"Saving cropped object {idx} with label {label_name} to: {crop_filename}")
        cv2.imwrite(crop_filename, crop_obj)