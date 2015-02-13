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

    Mat source_img;
    
    string addr = "../images/mono_000000%04d.png"; 
    VideoCapture seq;
	seq.open(addr);
    if(!seq.isOpened()) {
        cerr << "Unable to open Image Sequence" << endl;
        return -1;
    }
    while(1) {
        seq >> source_img;
        if(source_img.empty()) {
            cout << "End of Sequence "<<endl;
			break;
        }
        imshow("Image, Press any key to exit",source_img);
        waitKey(30);
    }
	cout << "End" <<endl;
    return 0;
}
    
