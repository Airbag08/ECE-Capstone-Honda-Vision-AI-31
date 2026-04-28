import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from ultralytics import YOLO
import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import time
import shutil
import gc

input_dir = r"C:\Users\arcis\OneDrive\Documents\RawVIN" #input folder for raw images
history_dir = r"C:\Users\arcis\OneDrive\Documents\VINHistory"  #history of raw images
output_dir = r"C:\Users\arcis\OneDrive\Documents\VINs"   #folder for processed annotated images
os.makedirs(output_dir, exist_ok=True)
os.makedirs(history_dir, exist_ok=True)

while True:
    #check for new images in the input directory every 5 seconds
    input_images = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
    ]
    #sleep if there are no new images
    if not input_images:
        print("No new images found. Checking again in 5 seconds...")
        time.sleep(5)
    #run prediction on every new image found in input directory
    else:
        print(f"\nFound new images. Processing...")

        model = YOLO(r"C:\Users\arcis\Downloads\622_12x_2144.pt")
        all_vins = []

        for filename in input_images:
            input_path = os.path.join(input_dir, filename)
            print("Processing:", input_path)

            results = model(input_path, device=0, batch=1, imgsz=1536) #1536

            for img_idx, r in enumerate(results):
                print(f"\n===== IMAGE {img_idx + 1} =====")

                # original image (BGR)
                img = r.orig_img.copy()

                boxes = r.boxes.xyxy
                classes = r.boxes.cls
                confs = r.boxes.conf
                names = r.names

                detections = list(zip(boxes, classes, confs))

                # sort left → right (critical for VIN order)
                detections = sorted(detections, key=lambda d: d[0][0])

                vin_chars = []
                flagged = False #flags VIN with low confidence characters for review

                for box, cls, conf in detections:
                    x1, y1, x2, y2 = map(int, box.tolist())
                    cls_id = int(cls)
                    conf = float(conf)
                    cls_name = names[cls_id]

                    vin_chars.append(cls_name)

                    #color bounding boxes based on confidence scores, using RGB for better readability
                    if conf < .69:
                        color = (255, 0, 0) #red
                        flagged = True 
                    elif conf < .79:
                        color = (255, 255, 0) #yellow
                        flagged = True
                    else:
                        color = (0, 255, 0) #green 

                    # ---- DRAW BOX (thin) ----
                    cv2.rectangle(
                        img,
                        (x1, y1),
                        (x2, y2),
                        color,
                        1
                    )

                    # ---- SMALL LABEL ABOVE BOX ----
                    label = f"{cls_name} {conf:.2f}"
                    cv2.putText(
                        img,
                        label,
                        (x1, max(y1 - 3, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,            # SMALL font
                        color,
                        1,
                        cv2.LINE_AA
                    )

                    print(f"{cls_name} conf={conf:.2f} box=({x1},{y1},{x2},{y2})")

                vin_string = "".join(vin_chars)
                all_vins.append(vin_string)

                # ---- DRAW FULL VIN ON IMAGE ----
                cv2.putText(
                    img,
                    f"VIN: {vin_string}",
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2,
                    cv2.LINE_AA
                )

                print("Predicted VIN:", vin_string)

                # ---- DISPLAY WITH MATPLOTLIB ----
                x_left = int(detections[0][0][0])      # first box x1
                x_right = int(detections[-1][0][2])    # last box x2

                y_top = int(min([box[0][1] for box in detections]))
                y_bottom = int(max([box[0][3] for box in detections]))

            # ---- ADD PADDING ----
                pad_x = 80
                pad_y = 40

                x_left = max(0, x_left - pad_x)
                x_right = min(img.shape[1], x_right + pad_x)

                y_top = max(0, y_top - pad_y)
                y_bottom = min(img.shape[0], y_bottom + pad_y)

            # ---- CROP IMAGE (ZOOM INTO VIN) ----
                vin_crop = img[y_top:y_bottom, x_left:x_right]

                # ---- DISPLAY WITH MATPLOTLIB ----
                vin_rgb = cv2.cvtColor(vin_crop, cv2.COLOR_BGR2RGB)
                plt.figure(figsize=(14,4))
                plt.imshow(vin_rgb)
                plt.axis("off")
                plt.close('all')
                #plt.show()
                original_filename = os.path.basename(r.path)
                name, ext = os.path.splitext(original_filename)

                if flagged:
                    name += "_FLAGGED"

                output_path = os.path.join(output_dir, f"{vin_string}_{name}.jpg")

                success = cv2.imwrite(output_path, vin_rgb)

                print("Saving to:", output_path)
                print("Save success:", success)

                shutil.move(r.path, os.path.join(history_dir, os.path.basename(r.path)))
                plt.close('all')
                del img
                del vin_crop
                del vin_rgb
                gc.collect()
                #plt.show()

            print("\n===== ALL VINS =====")
            for vin in all_vins:
                print(vin)
