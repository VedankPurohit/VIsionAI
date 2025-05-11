from ultralytics import YOLO
import cv2
import os
import numpy as np
from Modules.Segmentation.DownScale import downscale_image

def ObjectSegmentation(model, image_path, confidence_threshold, save_dir, patch_size = 640):
    assert os.path.isfile(image_path), "Image file not found"
    assert 0 <= confidence_threshold <= 1, "Confidence threshold must be between 0 and 1"

    im0 = cv2.imread(image_path)
    assert im0 is not None, f"Unable to read image: {image_path}"

    h, w, _ = im0.shape
    
    if h > patch_size or w > patch_size:
        patches = []
        for y in range(0, h, patch_size):
            for x in range(0, w, patch_size):
                patch = im0[y:y+patch_size, x:x+patch_size]
                patches.append(patch)
    else:
        patches = [im0]

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Directory '{save_dir}' created.")

    for patch_idx, patch in enumerate(patches, start=1):
        print(f"Processing patch {patch_idx}/{len(patches)}")

        results = model.predict(patch, show=False)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        clss = results[0].boxes.cls.cpu().numpy()
        confs = results[0].boxes.conf.cpu().numpy()

        # Convert patch to contiguous array
        patch = np.ascontiguousarray(patch)

        for idx, (box, cls, conf) in enumerate(zip(boxes, clss, confs), start=1):
            if conf > confidence_threshold:
                label_name = model.names[int(cls)]
                print(f"Detected object {idx} with class: {label_name} and confidence: {conf}")
                crop_obj = patch[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                crop_filename = os.path.join(save_dir, f"{label_name}_{patch_idx}_{idx}.png")
                print(f"Saving cropped object {idx} with label {label_name} to: {crop_filename}")
                cv2.imwrite(crop_filename, crop_obj)



model = YOLO("Models/yolov8l.pt")
image_path = "Tests\Realme 11 Pro plus in_11.jpeg"
confidence_threshold = 0.3
save_dir = "Results"
DownScaledImg = save_dir+"/1ImageDownScale.png"

if __name__ == "__main__":
    downscale_image(image_path, DownScaledImg)
    ObjectSegmentation(model, image_path, confidence_threshold, save_dir, 30000)