//** Sethu Chidambaram **//
//** Lane Detection **//

#include <stdio.h>
#include <dirent.h>
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <string>

using namespace std;
using namespace cv;


int main() {

    Mat source_img, img;
	// Source Image Stream Initialization
    string addr = "../images/mono_000000%04d.png"; 
    VideoCapture seq;
	seq.open(addr);
    if(!seq.isOpened()) {
        cerr << "Unable to open Image Sequence" << endl;
        return -1;
    }

	//Canny Temp Variables
	Mat dst, detected_edges;
	int edgeThresh = 1;
	int Threshold = 25;
	int ratio = 2;
	int kernel_size = 3;
	char* window_name = "Edge Map";
	// Create a temp all black image


	// Do until end of image stream
    while(1) {
		dst.create( 600, 1200, CV_8UC1);
		dst = Scalar::all(0);
		//For each Source Image
        seq >> source_img;		 
        if(source_img.empty()) {
            cout << "End of Sequence "<<endl;
			break;
        }
		// Crop image since upper half is not needed
		img = source_img(Rect( 0, 600, 1600, 600) ); 
		blur( img, detected_edges, Size(5,5) );
		Canny( detected_edges, detected_edges, Threshold, Threshold*ratio, kernel_size );

		// Do Hough Transform
		double rho = 1;
		double theta = CV_PI/180;
		


		img.copyTo( dst, detected_edges);
        imshow("Image", dst);
        char key = waitKey(30);
		if(key == 'z') break;
    }
	cout << "End" <<endl;
    return 0;
}
    
