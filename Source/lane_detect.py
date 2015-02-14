#! /usr/bin/env python
from __future__ import division

import os
import sys
import csv
import cv2
import glob
import numpy as np

def angle( x1, y1, x2, y2 ):
    val = (y2-y1)/(x2-x1)
    val = np.arctan(val)
    val = (val*180/3.14)%360
    if x2<x1:
        val = val + 180
    if val < 0:
        val = 360 + val
    return val

if __name__ == "__main__":
    i = 0
    cv2.namedWindow('Lane Markers')
    imgs = glob.glob("../images/mono_000000*.png")
     
    intercepts = []
    
    #Canny Parameters
    c_UppThreshold = 125
    c_LowThreshold = 15
    
    #Hough Parameters
    h_rho = 1
    h_theta = np.pi/180
    h_threshold = 100
    h_minLineLength = 200
    h_maxLineGap = 5
    
    #Intercept Threshold
    X_Threshold = 200
    
    for fname in sorted(imgs):
        i = i+1
        print "Image", i
        # Load image and prepare output image
        src_img = cv2.imread(fname)

        #Crop Image
        img = src_img[ 600:1200, 0:1600]  	#y:h,x:w
        #thresholding to inprove contrast
        cv2.threshold(img, 127, 255, 3)
        
        #Blur Image
        img = cv2.blur( img, (5,5))
        #Apply Canny Edge Detector
        edge = cv2.Canny( img, c_LowThreshold, c_UppThreshold)
        #Detect Hough Lines
        lines = cv2.HoughLinesP( edge, h_rho, h_theta, h_threshold, h_minLineLength, h_maxLineGap )
        if not (lines is None):
            LminX, LminY, RminX, RminY = 200,200,1400,200
            Lcontrol, Rcontrol = 0,0
            for x1,y1,x2,y2 in lines[0]:
                ang = angle( x1, y1, x2, y2 )
                if (ang > 20 and ang < 160) or (ang > 200 and ang < 340):
                    cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
                    if y1 > LminY:
                        if Lcontrol < 1 and (x1 < LminX+X_Threshold+300) and (x1 > LminX-X_Threshold):
                            Lcontrol = Lcontrol+1
                            LminY = y1
                            LminX = x1
                        elif (x1 < LminX+X_Threshold+100) and (x1 > LminX-X_Threshold):
                            LminY = y1
                            LminX = x1
                    if y1 > RminY:
                        if Rcontrol < 1 and (x1 < RminX+X_Threshold) and (x1 > RminX-X_Threshold-300) :
                            Rcontrol = Rcontrol+1
                            RminY = y1
                            RminX = x1
                        elif (x1 < RminX+X_Threshold) and (x1 > RminX-X_Threshold-100):
                            RminY = y1
                            RminX = x1                  
            cv2.circle(img, (LminX, LminY), 3, (255,0,0), 3)
            cv2.circle(img, (RminX, RminY), 3, (255,0,0), 3)
            if LminX == 200:
                LminX =  "None"
            if RminX == 1400:
                RminX = "None"
            intercepts.append((os.path.basename(fname), LminX, RminX))
 
        
        # Show image
        # Threshold Lines:
        cv2.line(img,(50,0),(50,600),(0,255,0),2)
        cv2.line(img,(350,0),(350,600),(0,255,0),2)
        cv2.line(img,(1250,0),(1250,600),(0,255,0),2)
        cv2.line(img,(1550,0),(1550,600),(0,255,0),2)
        
        #cv2.imshow('Edges', edge)
        cv2.imshow('Lane Markers', img)
        key = cv2.waitKey(30)
        if key == 27:
            sys.exit(0)
                 
    # CSV output
    #with open('intercepts.csv', 'w') as f:
        #writer = csv.writer(f)   
        #writer.writerows(intercepts)
         
    cv2.destroyAllWindows();
