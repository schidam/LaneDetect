#! /usr/bin/env python
from __future__ import division

import os
import sys
import csv
import cv2
import glob
import numpy as np

# Function to return the angle of the line between two points
def angle( x1, y1, x2, y2 ):
    if x2-x1 != 0:
        val = (y2-y1)/(x2-x1)
        val = np.arctan(val)
    else:
        val = 3.14/2  #x2-x1=0 => angle = pi/2
    # convert to radians
    val = (val*180/3.14)%360
    # detect direction fo angle
    if x2<x1:
        val = val + 180
    # ajust value to 0-360 degrees
    if val < 0:
        val = 360 + val
    return val

if __name__ == "__main__":
    i = 0
    cv2.namedWindow('Lane Markers')
    imgs = glob.glob("../images/mono_000000*.png")
     
    intercepts = []
    
    # Canny Parameters
    c_UppThreshold = 125
    c_LowThreshold = 15
    
    # Hough Parameters
    h_rho = 5
    h_theta = np.pi/180
    h_threshold = 100
    h_minLineLength = 200
    h_maxLineGap = 5
    
    # Intercept Threshold
    X_Threshold = 200
    
    # Lane Detection Threshold
    Lane_Threshold = 120
    LminX_init = 200
    LminY_init = 0
    RminX_init = 1400
    RminY_init = 0
    for fname in sorted(imgs):
        i = i+1
        print "Image", i
        # Load image and prepare output image
        src_img = cv2.imread(fname)

        # Crop Image
        img = src_img[ 600:1200, 0:1600]  	#y:h,x:w
        
        # Blur Image
        img = cv2.GaussianBlur( img, (5,5), 0)
        img = cv2.medianBlur( img, 5)
        
        # Apply Canny Edge Detector
        edge = cv2.Canny( img, c_LowThreshold, c_UppThreshold)     
           
        # Detect Hough Lines
        lines = cv2.HoughLinesP( edge, h_rho, h_theta, h_threshold, h_minLineLength, h_maxLineGap )
        
        if not (lines is None):
            LminX, LminY, RminX, RminY = LminX_init, LminY_init, RminX_init, RminY_init
            Lcontrol, Rcontrol = 0,0
            temp_angL,temp_angR = 0,0
            # Iterate through each hough line detected
            for x1,y1,x2,y2 in lines[0]:
                # find angle
                ang = angle( x1, y1, x2, y2 )
                # Ignore horizontal lines
                if (ang > 15 and ang < 165) or (ang > 195 and ang < 345):
                    # CHeck which point is lower (x1,y1) or (x2,y2)
                    if y1>y2:
                        temp_x = x1
                        temp_y = y1
                    else:
                        temp_x = x2
                        temp_y = y2
                    # If the image pixel is white(light grey)
                    if img[temp_y,temp_x,0] > Lane_Threshold:
                        # Draw line on image
                        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
                        #cv2.circle(img, (x1, y1), 3, (0,0,255), 3)
                        #cv2.circle(img, (x2, y2), 3, (127,127,127), 3)
                        # Find Left X_intercept                        
                        if temp_y > LminY:
                            # Accept First value for estimation
                            if Lcontrol < 1 and (temp_x < LminX+X_Threshold+300) and (temp_x > LminX-X_Threshold+10) and ang > 300:
                                Lcontrol = Lcontrol+1
                                LminY = temp_y
                                LminX = temp_x
                                temp_angL=ang
                            elif (temp_x < LminX+X_Threshold+100) and (temp_x > LminX-X_Threshold) and ang > 300:
                                LminY = temp_y
                                LminX = temp_x
                                temp_angL=ang
                        # Find Right X_Intercept
                        if temp_y > RminY:
                            if Rcontrol < 1 and (temp_x < RminX+X_Threshold-10) and (temp_x > RminX-X_Threshold-300) and ang < 100:
                                Rcontrol = Rcontrol+1
                                RminY = temp_y
                                RminX = temp_x
                                temp_angR=ang
                            elif (temp_x < RminX+X_Threshold) and (temp_x > RminX-X_Threshold-100) and ang < 100:
                                RminY = temp_y
                                RminX = temp_x
                                temp_angR=ang
            # print temp_angL,temp_angR
            # Show the tracked points on image                                      
            cv2.circle(img, (LminX, LminY), 3, (255,0,0), 3)
            cv2.circle(img, (RminX, RminY), 3, (255,0,0), 3)
            if LminX == LminX_init:
                LminX =  "None"
            if RminX == RminX_init:
                RminX = "None"
            intercepts.append((os.path.basename(fname), LminX, RminX))    
        # Show image 
        # cv2.imshow('Edges', edge)
        cv2.imshow('Lane Markers', img)
        key = cv2.waitKey(30)
        if key == 27:
            sys.exit(0)
                 
    # CSV output
    with open('intercepts.csv', 'w') as f:
        writer = csv.writer(f)   
        writer.writerows(intercepts)
         
    cv2.destroyAllWindows();
