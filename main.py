import sys
import cv2
import numpy as np
import mediapipe as mp
from joblib import load
from sklearn.ensemble import RandomForestClassifier
#Initialize mediapipe pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

def getFeatures(landmarks):
    """Convert the Pose Landmarks into features for classifier
    
    Parameters:
        landmarks ('google.protobuf.pyext._message.RepeatedCompositeContainer'): Pose Landmarks from image using mediapipe
    
    Returns:
        np.array: array of features for classifier"""

    #initialize lists
    lMs = []
    lMs2 = []
    #enumerate landmarks and split into distinct values
    for id, lm in enumerate(landmarks):
        lMs.append(str(lm).split('\n'))

    #remove empty entries and convert to floats and explode to new list
    for i in range(11, len(lMs)):
        while ('' in lMs[i]):
            lMs[i].remove('')
        lMs2.append(float(lMs[i][0].replace('x: ', '')))
        lMs2.append(float(lMs[i][1].replace('y: ', '')))
        lMs2.append(float(lMs[i][2].replace('z: ', '')))
        lMs2.append(float(lMs[i][3].replace('visibility: ', '')))
    
    return np.array(lMs2).reshape(1, -1)

def intToExercise(x):
    """Converts classification integer into exercise name

    Parameters:
        x (int): classifications return value
    
    Returns:
        str: Name of exercise"""

    if x == 0:
        return('pushup')
    elif x == 1:
        return('bent over row')
    elif x == 2:
        return('chest dips')
    elif x == 3:
        return('glute bridge')
    elif x == 4:
        return('lunges')
    elif x == 5:
        return('plank')
    elif x == 6:
        return('pullup')
    elif x == 7:
        return('shoulder press')
    elif x == 8:
        return('squat')
    return None

def main(argv):
    #only allow one photo at a time
    if not len(argv) == 1:
        print("Argument Error: Please enter only one file.")
        exit()

    #load image (resize for display purposes)
    img = cv2.imread(argv[0])
    img = cv2.resize(img, (0, 0), None, .75, .75)
    imgPose = img.copy()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #get pose as results
    results = pose.process(imgRGB)

    #if there is pose, draw pose estimations
    if results.pose_landmarks:
        mpDraw.draw_landmarks(imgPose, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = imgPose.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(imgPose, (cx, cy), 5, (255,0,0), cv2.FILLED)

    #get features
    features = getFeatures(results.pose_landmarks.landmark)

    #load model
    classifier = load('exerciseImageClassifier.joblib')

    #predict exercise type
    pred = intToExercise(classifier.predict(features))

    #create vertical stack of images for comparison and add predicted text
    res = np.vstack((img, imgPose))
    res = cv2.putText(res, pred, (25, 50), cv2.FONT_HERSHEY_SIMPLEX,
                      1, (0,0,255), 2, cv2.LINE_AA)

    while True:
        cv2.imshow("Image", res)
        cv2.waitKey(1)

if __name__ == '__main__':
    main(sys.argv[1:])