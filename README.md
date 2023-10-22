# Exercises-Prediction-Model
Python and opencv to predict the type of exercise from an image.

collectImages.py: script used to collect images from google images
exerciseImageClassifier.joblib: RandomTreeClassifier trained to classify images using pose estimation (see poseEst.ipynb)
imagePoses.csv: file containing base64 encoding of exercisse images along with pose estimations and exercise type (see poseEst.ipynb)
main.py: script to demonstrate model functionality using OpenCV
poseEst.ipynb: Jupyter Notebook documenting analysis of imagePoses.csv and train/test of exerciseImageClassifier.joblib
poseToCSV.py: converts exercise photos to imagePoses.csv (see poseEst.ipynb for columns)
