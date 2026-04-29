# ECE-Capstone-Honda-Vision-AI-31

Ignition GUI, Python code, and supplemental images that allow OCR to perform VIN recognition.

This product automates the process of reading raw underbody VIN images from vehicles in production. The system takes a VIN image, predicts the VIN string, creates an annotated output image, and displays the result in Ignition. The Ignition HMI allows the user to view the VIN history, select previous scans, edit a VIN if needed, and review flagged images.

The following sections explain how to use and maintain the system. The Requirements section lists the software needed to run the product. The How to Operate the System section explains how to run the Python prediction software and use the Ignition HMI. The Features section explains the VIN table, annotated image display, VIN editing, table refresh, and flagging system. The Basic Troubleshooting section covers common user issues, while the Maintenance and Engineering Troubleshooting sections provide guidance for keeping the system working properly.

---

## Product Usage

## Requirements

- Windows OS
- Python environment
- Ignition
- A GPU accessible by a computer

---

## 5.1 How to Operate the System

### Prediction Software

1. Download the Python file and trained model file.
2. Open the Python environment and open the prediction software file within the environment.
3. Install the required Python libraries, including Ultralytics and GPU-compatible Torchvision/Torchaudio.
4. Ensure the trained model’s local location is set to `model`.
5. Set the directories for `input_dir`, `output_dir`, and `history_dir` to folder locations accessible on the local device.
6. Run the Python program.
7. Move images into the input folder to have the VIN predicted.

### Ignition

1. Download and launch the HondaVIN project.
2. Change the custom property `annotatedFolder` to the correct folder path. `convertPath.py` can be used to convert the path to Ignition format.
3. Save and launch the project.
4. Click any row in the table to display that row’s annotated VIN image.
5. Use the Previous and Next buttons to move through the image history.
6. Review any row marked `FLAGGED` in the flag column.
7. If a VIN prediction is incorrect, edit the VIN cell directly in the table.
8. If needed, toggle the flag status to mark or unmark an image for later review.

---

## Features

### Flagging System

The system automatically flags images when a character confidence score is below `0.80` or when the detected VIN length is not 17 characters. Flagged files are marked with the `_FLAGGED` suffix, and the Ignition table displays them with a red flag cell.

### VIN Editing in Ignition Table

The VIN value can be edited directly in the Ignition table. This allows the user to correct a prediction if the model reads a character incorrectly.

### Automatic Table Refresh

The frontend uses a RescanTimer to refresh the table. This allows newly processed images to appear in the HMI without restarting the project.

---

## 5.2 Basic Troubleshooting and Common Issues

### Problem 1: Software Cannot Find the Input Folder

**Detection:** Images are in the input folder, but the code repeats the “no images found” message.

**Solution:** Ensure the directory set within the Python file `input_dir` is either of the following:

- The full file path from the C: drive. Preferred.
- A file path accessible within the Python environment being used.

### Problem 2: Output Images Are Blurry or Have No Detections

**Detection:** The code runs, but the images in the output folder are blurry or missing detections.

**Solution:** Ensure the images placed into the input folder have dimensions of `4200x2128`. If the images were already processed, they can be found in the history folder.

### Problem 3: Annotated Image Does Not Display in Ignition

**Detection:** The VIN table and the image component are blank.

**Solution:** Check that the folder path stored in the custom property `annotatedFolder` is in the correct format for Ignition.

### Problem 4: Table Does Not Update with New Images

**Detection:** New images are placed in the raw VIN folder, but the annotated images do not appear in the HMI.

**Solution:** Make sure the backend Python program is running while using the HMI.

---

## Maintenance

The system does not require physical maintenance, but the software folders and file paths should be checked regularly. The input, output, and history folders should be kept organized so the backend and frontend can find the correct files. If the amount of stored image data becomes too large, older images should be archived according to Honda’s storage rules.

The model should also be retested if new image conditions are introduced, such as different lighting, camera angles, camera resolution, or VIN plate appearances. If accuracy drops, additional images should be annotated and used to retrain the model. The Ignition project should also be backed up after major script or interface changes.

---

## 5.3 Engineering Troubleshooting Report

### Problem 1: Missing or Outdated Python Dependencies

**Cause:** The backend prediction software may fail to run if required Python libraries are missing, outdated, or installed in the wrong environment. This can happen after moving the project to a new computer, updating Python, or creating a new virtual environment.

**Solution:** Run the required `pip install` commands again to reinstall or update the dependencies. Make sure the installs are completed in the same Python environment used to run the backend software. If a library is outdated, install the latest version using the upgrade command.

### Problem 2: VIN Parsing Error

**Cause:** The filename format may not match the expected pattern. This can prevent the frontend from extracting the VIN, date, and time correctly.

**Solution:** Make sure output images follow the expected naming format. The parser should also ignore the `_FLAGGED` suffix before extracting the VIN and timestamp.

### Problem 3: Low Model Confidence on Certain Characters

**Cause:** Some VIN characters may be harder to detect because of lighting, blur, or limited training examples.

**Solution:** Add more annotated examples of difficult characters to the dataset and retrain the model. Images with low confidence should stay flagged for review.

---

## GPU Compatibility

To make this program GPU compatible, run these bash commands:

```bash
pip uninstall torch torchvision torchaudio

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
