# ECE-Capstone-Honda-Vision-AI-31
Ignition GUI + Python Code + Supplemental Images that allow the OCR to perform on VINs

This product automates the process of reading raw underbody VIN images from vehicles in production. The system takes a VIN image, predicts the VIN string, creates an annotated output image, and displays the result in Ignition. The Ignition HMI allows the user to view the VIN history, select previous scans, edit a VIN if needed, and review flagged images.
The following sections explain how to use and maintain the system. The Requirements section lists the software needed to run the product. The How to Operate the System section explains how to run the Python prediction software and use the Ignition HMI. The Features section explains the VIN table, annotated image display, VIN editing, table refresh, and flagging system. The Basic Troubleshooting section covers common user issues, while the Maintenance and Engineering Troubleshooting sections provide guidance for keeping the system working properly. 
 
Product Usage  

Requirements  
•	Windows OS
•	Python environment
•	Ignition
•	A GPU accessible by a computer
    
5.1 How to operate the system 
Prediction Software:
1.	Download the Python file and trained model file.
2.	Open Python environment and open the prediction software file within the environment.
3.	Install required Python Libraries including Ultralytics and GPU compatible Torchvision/Torchaudio
4.	Ensure the trained model’s location is within the Python environment
5.	Set the image directories to locations accessible on the local device.
6.	Run the Python program.
7.	Move images into the input folder to have the VIN predicted.

Ignition:
1.	Download and launch the HondaVIN project.
2.	Change the custom property annotatedFolder to the correct folder path (convertPath.py can be used to convert to Ignition format)
3.	Save and launch project.
4.	Click any row in the table to display that row’s annotated VIN image.
5.	Use the Previous and Next buttons to move through the image history.
6.	Review any row marked “FLAGGED” in the flag column.
7.	If a VIN prediction is incorrect, edit the VIN cell directly in the table.
8.	If needed, toggle the flag status to mark or unmark an image for later review.
   
Features  
•	Flagging System
The system automatically flags images when a character confidence score is below 0.80 or when the detected VIN length is not 17 characters. Flagged files are marked with the “_FLAGGED” suffix, and the Ignition table displays them with a red flag cell.
•	VIN Editing in Ignition Table
The VIN value can be edited directly in the Ignition table. This allows the user to correct a prediction if the model reads a character incorrectly.
•	Automatic Table Refresh
The frontend uses a RescanTimer to refresh the table. This allows newly processed images to appear in the HMI without restarting the project.

5.2 Basic trouble shooting and common issues 
Problem 1
Software cannot find the input folder. 
Detection: Images are in the input folder, but the code repeats the “no images found” message.

Solution: Ensure the directory set within the python file “input_dir” is either of the two below:
•	The full file path from the C: drive. (preferred)
•	A file path accessible within the python environment being used.

Problem 2
The output images are blurry/have no detections
Detection: The code runs, but the images in the output folder are blurry or missing detections. 

Solution: Ensure the images put into the input folder (which can be found in the history folder if already processed) have dimensions 4200x2128.

Problem 3
Annotated image does not display in Ignition
Detection: The VIN table and the image component are blank

Solution: Check that the folder path stored in the custom property annotatedFolder is in the correct format for Ignition

Problem 4
Table does not update with new images
Detection: New images are put in the raw VIN folder, but the annotated images do not appear in the HMI
Solution: Make sure the backend Python program is running while using the HMI
  
Maintenance  
The system does not require physical maintenance, but the software folders and file paths should be checked regularly. The input, output, and history folders should be kept organized so the backend and frontend can find the correct files. If the amount of stored image data becomes too large, older images should be archived according to Honda’s storage rules.
The model should also be retested if new image conditions are introduced, such as different lighting, camera angles, camera resolution, or VIN plate appearances. If accuracy drops, additional images should be annotated and used to retrain the model. The Ignition project should also be backed up after major script or interface changes.
5.3 Engineering Troubleshooting report  
Problem 1 
Missing or Outdated Python Dependencies
Cause: The backend prediction software may fail to run if required Python libraries are missing, outdated, or installed in the wrong environment. This can happen after moving the project to a new computer, updating Python, or creating a new virtual environment.

Solution: Run the required pip install commands again to reinstall or update the dependencies. Make sure the installs are completed in the same Python environment used to run the backend software. If a library is outdated, install the latest version using the upgrade command.



Problem 2 
VIN parsing error
Cause: The filename format may not match the expected pattern. This can prevent the frontend from extracting the VIN, date, and time correctly.

Solution: Make sure output images follow the expected naming format. The parser should also ignore the “_FLAGGED” suffix before extracting the VIN and timestamp.

Problem 3 
Low model confidence on certain characters
Cause: Some VIN characters may be harder to detect because of lighting, blur, or limited training examples.

Solution: Add more annotated examples of difficult characters to the dataset and retrain the model. Images with low confidence should stay flagged for review.



TO MAKE THIS PROGRAM GPU COMPATIBLE, run these bash commands:

pip uninstall torch torchvision torchaudio

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
 
