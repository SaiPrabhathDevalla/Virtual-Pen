import numpy as np
import cv2
from collections import deque

# -------------------- TRACKBAR CALLBACK --------------------
def setValues(x):
    pass

# -------------------- COLOR TRACKBARS --------------------
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)

# -------------------- POINT STORAGE --------------------
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = green_index = red_index = yellow_index = 0

kernel = np.ones((5,5), np.uint8)

colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
color_names = ["BLUE","GREEN","RED","YELLOW"]
colorIndex = 0

# -------------------- BLACK DRAWING BOARD --------------------
paintWindow = np.zeros((471,636,3), dtype=np.uint8)

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0)

# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Read HSV range
    Upper_hsv = np.array([
        cv2.getTrackbarPos("Upper Hue", "Color detectors"),
        cv2.getTrackbarPos("Upper Saturation", "Color detectors"),
        cv2.getTrackbarPos("Upper Value", "Color detectors")
    ])
    Lower_hsv = np.array([
        cv2.getTrackbarPos("Lower Hue", "Color detectors"),
        cv2.getTrackbarPos("Lower Saturation", "Color detectors"),
        cv2.getTrackbarPos("Lower Value", "Color detectors")
    ])

    # -------------------- UI BUTTONS --------------------
    frame = cv2.rectangle(frame,(40,1),(140,65),(122,122,122),-1)
    frame = cv2.rectangle(frame,(160,1),(255,65),colors[0],-1)
    frame = cv2.rectangle(frame,(275,1),(370,65),colors[1],-1)
    frame = cv2.rectangle(frame,(390,1),(485,65),colors[2],-1)
    frame = cv2.rectangle(frame,(505,1),(600,65),colors[3],-1)

    cv2.putText(frame,"CLEAR",(49,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    cv2.putText(frame,"BLUE",(180,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    cv2.putText(frame,"GREEN",(285,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    cv2.putText(frame,"RED",(420,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    cv2.putText(frame,"YELLOW",(515,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

    # -------------------- MASK --------------------
    mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    cnts,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) > 0:
        cnt = max(cnts, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)

        M = cv2.moments(cnt)
        if M["m00"] != 0:
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

            if center[1] <= 65:
                if 40 <= center[0] <= 140:
                    bpoints=[deque(maxlen=1024)]
                    gpoints=[deque(maxlen=1024)]
                    rpoints=[deque(maxlen=1024)]
                    ypoints=[deque(maxlen=1024)]
                    blue_index=green_index=red_index=yellow_index=0
                    paintWindow[:] = 0
                elif 160 <= center[0] <= 255:
                    colorIndex = 0
                elif 275 <= center[0] <= 370:
                    colorIndex = 1
                elif 390 <= center[0] <= 485:
                    colorIndex = 2
                elif 505 <= center[0] <= 600:
                    colorIndex = 3
            else:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=1024)); blue_index+=1
        gpoints.append(deque(maxlen=1024)); green_index+=1
        rpoints.append(deque(maxlen=1024)); red_index+=1
        ypoints.append(deque(maxlen=1024)); yellow_index+=1

    # -------------------- DRAWING --------------------
    points = [bpoints,gpoints,rpoints,ypoints]
    for i in range(4):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(paintWindow,points[i][j][k-1],points[i][j][k],colors[i],3)

    # -------------------- STATUS TEXT --------------------
    cv2.putText(frame,"STATUS: DRAWING",(10,110),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.putText(frame,f"COLOR: {color_names[colorIndex]}",(10,150),
                cv2.FONT_HERSHEY_SIMPLEX,1,colors[colorIndex],2)

    # -------------------- FINAL OUTPUT (FIXED SIZE) --------------------
    paint_resized = cv2.resize(paintWindow, (frame.shape[1], frame.shape[0]))
    overlay = cv2.addWeighted(frame, 1, paint_resized, 0.4, 0)
    final_output = np.hstack((paint_resized, overlay))

    cv2.imshow("VIRTUAL PEN", final_output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
