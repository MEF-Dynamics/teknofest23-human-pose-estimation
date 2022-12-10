import cv2
import math
import numpy as np
import mediapipe as mp

def findDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def findAngle(x1, y1, x2, y2):
    theta = math.acos((y2 - y1) * (-y1) / (math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / math.pi) * theta
    return degree

font = cv2.FONT_HERSHEY_SIMPLEX

blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

logo = cv2.imread('logo.png')
logo_height, logo_width, _ = logo.shape
logo_dvider = 25
logo_height = int(logo_height / logo_dvider)
logo_width = int(logo_width / logo_dvider)
logo = cv2.resize(logo, (logo_width, logo_height))

logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)

if __name__ == "__main__":
    # 0           -> webcam
    # 'video.mp4' -> video file
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Null.Frames")
            break
        try:
            h, w = image.shape[:2]

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            keypoints = pose.process(image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            neck_to_back = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            body_to_back = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
            cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
            cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            if neck_to_back < 40 and body_to_back < 10:
                color = green
                # Add "Duruş bozukluğu yok" text to top right corner
                cv2.putText(image, 'Durus Bozuklugu Yok', (w - 400, 50), font, 1, color, 2)

            else:
                color = red
                cv2.putText(image, 'Durusunuz Bozuk !!!', (w - 400, 50), font, 1, color, 2)
                cv2.putText(image, 'Durusunuzu Duzeltin', (w - 400, 80), font, 1, color, 2)

            cv2.putText(image, str(int(neck_to_back)), (l_shldr_x + 10, l_shldr_y), font, 0.9, color, 2)
            cv2.putText(image, str(int(body_to_back)), (l_hip_x + 10, l_hip_y), font, 0.9, color, 2)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), color, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), color, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), color, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), color, 4)

        except:
            pass
        
        roi = image[0:logo_height, 0:logo_width]
        roi[np.where(logo_gray != 255)] = logo[np.where(logo_gray != 255)]

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
