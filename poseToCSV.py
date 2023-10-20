import os
import cv2 as cv
import base64
import mediapipe as mp
import csv
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

#directories
dirs = ['pushup', 'pullup', 'chest-dips', 'bent-over-row', 
             'shoulder-press', 'squat', 'lunges', 'plank', 'glute-bridge']

#rows
rows_list = [['imageName', 'base64encoded', 'imageWidth', 'imageHeight', 'poseLandmarks', 'excercise']]

#loop thru directories
for dir in dirs:
    #list of images in directory
    images = os.listdir(dir)
    
    #get pose estimation for each image
    for image in images:
        #initialize list for data
        data = []

        data.append(image)

        path = dir + '/' + image
        src = cv.imread(path)
        
        with open(path, 'rb') as image_file:
            data.append(base64.b64encode(image_file.read()))

        w, h, c, = src.shape

        data.append(w)
        data.append(h)

        #create pose landmarks
        results = pose.process(src)
        if results.pose_landmarks:
            #initialize poseLandmarks list
            poseLandmarks = []
            mpDraw.draw_landmarks(src, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                
                #add poseLandmark to list
                poseLandmarks.append(str(lm).replace('\n', ','))
            
            data.append(poseLandmarks)
        else:   
            data.append(None)
        
        data.append(dir.replace('-', ' '))
        
        rows_list.append(data)
        print('DONE')


with open('imagePoses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows_list)
