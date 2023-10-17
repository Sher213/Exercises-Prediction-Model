import cv2 as cv
import mediapipe as mp
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

window_name = 'demo'

cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)

src = cv.imread('img_x.jpg')

results = pose.process(src)
if results.pose_landmarks:
    mpDraw.draw_landmarks(src, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    for id, lm in enumerate(results.pose_landmarks.landmark):
        h, w,c = src.shape
        cx, cy = int(lm.x*w), int(lm.y*h)
        cv.circle(src, (cx, cy), 5, (255,0,0), cv.FILLED)

while True:
    cv.imshow(window_name, src)
    cv.waitKey(1)
