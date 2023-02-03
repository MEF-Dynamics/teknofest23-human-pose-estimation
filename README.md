# Pose-Estimation-Application

### Description
* This is a pose estimation application with features that helps desk workers to detaily contract their muscles and joints to prevent injuries and to be able to do their work more effectively.

### Our Motivations
* Application motivations ;
    - To prevent the spread of Posture Disorder
    - Awareness of Posture Disorder: Creating Awareness
    - Effective Teaching of Posture Disorder

### Features
* Application constructed %100 python structure with Python Language and pythonist modules.
* Application also able to run predictions though the KeyMaps shown in ../Assets/Readme/Key Map.png file. Saved for future use.

### Structure
* Application is structured with 1 main part.
    - Detecting Pose Estimations
* Application is seperated into utilitiy methods that runs down the program much more effectively with threads and processes. Some of the utility method used in the application are ;
    - @pose_estimation
    - @get_available_cameras
* Application is constructed with a dynamical structure.
* Application is served with tkinter library for graphical user interface.

### Installation
>Application is reserved on a machine with RTX 3060 Laptop GPU and python 3.10.0 version.\

* Environment Setup
    * `conda create -n pose_app python==3.10.0`
    * `conda activate pose_app`
* PIP and Conda installation Steps
    * `pip install -r requirements.txt`

### Usage

* Application is ready to use after installation steps.

* After the "Login" window the two Applications will be available to use in order.

* To Run :
    * `conda activate sign_app`
    * `python main.py`

### Example Of Usage

![Example Of Usage](Assets/Readme/Merged_Images.png)

### TO:DO
- [ ] Add language support.
- [ ] Detail database.
- [ ] Modify model.
- [ ] Collect errors.
