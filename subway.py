#By sachin prajapati
import cv2 
import pyautogui
import numpy as np
#cv2 is main library used here in DIP Project for function like VideoCapture,
# inRange ,contours,drawing circle lines and many more
#pyautogui library is mainly used for press function help to press keys
#numpy is used for array
vid = cv2.VideoCapture(0)#cv2 function to start capturing video
prev_pos = "neutral"  #previous postion of moments(center of mass contours)

#function which take list of contours and return max area contour
def max_cnt(contours): 
    cnt = []   #index
    max_area = 0
    for i in contours:
        area = cv2.contourArea(contours[i])#area of contour
        if(area > max_area):
            cnt = i
            max_area = area
    return cnt #index of maximum area contour

while(1): 
    _, frame = vid.read() #a frame of video in infinite loop
    frame = cv2.flip(frame,1) #fliping the frame to avoid inversion
    frame = frame[:300,300:600] #croping frame to get only gesture if object
    frame = cv2.GaussianBlur(frame,(5,5),0) #reducing noise using Gaussian blur
    
    lower_skin = np.array([13,16,28]) #lower bound of rgb 
    upper_skin = np.array([87,93,125]) #lower bound of rgb 
    #these bounds are used to mask your hand or object color using which you are
    #going to control keys
    #These bound are first find using proj1 file

    mask = cv2.inRange(frame, lower_skin, upper_skin)#masking of bgr colors
    _,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)#thresholding of mask image

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #find contour points(sharp color changes point in thresholded image )
    #contour is the boundary of object or sharp color corner
    if len(contours) == 0: #if no coutour found
        continue #continue that frame
    
    max_contour = max(contours,key = cv2.contourArea) #get index of max area contour

    epsilon = 0.01*cv2.arcLength(max_contour,True)
    #the maximum distance between the approximation of a shape contour
    max_contour = cv2.approxPolyDP(max_contour,epsilon,True)#approximation of
    #maxcontour to get sharp contour
    
    M = cv2.moments(max_contour)#centroid of can say intertia or center of mass
    try:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
    #x and y are the coordinate of center of mass(M)
    except ZeroDivisionError: ##exception handling
        continue

    frame = cv2.circle(frame , (x,y) , 10 , (255,0,0) , 2)
    #shows a circle at x,y(M) of raduis 10 with blue color 
    frame = cv2.drawContours(frame, [max_contour], -1, (0,0,255), 3)
    #draw contour of list of max area contour on frame 
    frame = cv2.line(frame , (75,0) , (75,299) , (255,255,255) , 2)#vertical line at x=75
    frame = cv2.line(frame , (225,0) , (225,299) , (255,255,255) , 2)#vertical line at x=225
    frame = cv2.line(frame , (75,200) , (225,200) , (255,255,255) , 2)#horizontal line at y=200
    frame = cv2.line(frame , (75,250) , (225,250) , (255,255,255) , 2)#horizontal line at y=250
    # lines to divide area to understand controls

    cv2.imshow('image', frame)
    #shows the frame of video with lines ,contours ans a circle at centroid of maxarea contour

    #position of hand or object according to x,y
    #and keys are assigned according to these positions
    if x < 75: 
        curr_pos = "left"#left key is assigned to cur_pos
    elif x > 225:
        curr_pos = "right"
    elif y < 200 and x > 75 and x < 225:
        curr_pos = "up"
    elif y > 250 and x > 75 and x < 225:
        curr_pos = "down"
    else:
        curr_pos = "neutral"

    if curr_pos!=prev_pos: #postion of object does'nt change comparing to prev frame
        if curr_pos != "neutral": #not at centre segment of four lines
            pyautogui.press(curr_pos) #press function to press curr positon key
        prev_pos = curr_pos #store current position as previous position
    if cv2.waitKey(1) == ord('q'):#if pressed key is q 
    #waitkey give a pause before next frame if we press key it return ascii value of that key
    #ord function convert char to ascii
        break #then break the loo[]
vid.release() #release the video capturing
cv2.destroyAllWindows() #close all windows
