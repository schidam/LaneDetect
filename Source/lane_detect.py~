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
    c_threshold = 50 
    c_scaling = 4
    
    #Hough Parameters
    h_rho = 1
    h_theta = np.pi/180
    h_threshold = 100
    h_minLineLength = 200
    h_maxLineGap = 10
    
    for fname in sorted(imgs):
        i = i+1
        print "Image", i
        # Load image and prepare output image
        src_img = cv2.imread(fname)

        #Crop Image
        img = src_img[ 600:1200, 0:1600]  	#y:h,x:w
        #Blur Image
        img = cv2.blur( img, (5,5))
        #Apply Canny Edge Detector
        edge = cv2.Canny( img, c_threshold, c_threshold * c_scaling)
        #Detect Hough Lines
        lines = cv2.HoughLinesP( edge, h_rho, h_theta, h_threshold, h_minLineLength, h_maxLineGap )
        if not (lines is None):
            for x1,y1,x2,y2 in lines[0]:
                ang = angle( x1, y1, x2, y2 )
                if (ang > 20 and ang < 160) or (ang > 200 and ang < 340):
                    cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
                    print "yellow ",ang
                else:
                    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
                    print "green ",ang                    
        # Sample intercepts
        #intercepts.append((os.path.basename(fname), left_x, right_x))
 
        # Show image
        cv2.imshow('Edges', edge)
        cv2.imshow('Lane Markers', img)
        key = cv2.waitKey(50)
        if key == 27:
            sys.exit(0)
                 
    # CSV output
    #with open('intercepts.csv', 'w') as f:
        #writer = csv.writer(f)   
        #writer.writerows(intercepts)
         
    cv2.destroyAllWindows();
