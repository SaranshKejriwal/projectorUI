import freenect
import cv2
import numpy as np
#from functions import *

def nothing(x):
    pass

#cv2.namedWindow('edge')
cv2.namedWindow('thr')#order of namedWindow affects order of imshow
cv2.moveWindow('thr',500,600)

cv2.namedWindow('ui')
cv2.moveWindow('ui',0,0)
cv2.namedWindow('disparity')#order of namedWindow affects order of imshow
cv2.moveWindow('disparity',800,600)

#cv2.namedWindow('Input')
#cv2.moveWindow('Input',0,600)
cv2.createTrackbar('low_th', 'thr', 220, 255, nothing)
cv2.createTrackbar('high_th', 'thr', 223, 255, nothing)
#cv2.namedWindow('Win')
kernel = np.ones((5, 5), np.uint8)


print('Press \'b\' in window to stop')
ui=cv2.imread("ui_blank2.jpg")
count=0
#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	count=count+1
	
	ui=cv2.imread("ui_blank.jpg")
	#Scaling Ref rects_________________________________________
	cv2.rectangle(ui,(0,0),(640,480),(155,255,255),2)
	cv2.rectangle(ui,(0,0),(1366,768),(155,255,255),2)

	#UI buttons_____________________________________________________
	cv2.rectangle(ui,(320,150),(370,200),(0,255,255),6)
	cv2.putText(ui,"D",(335,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
	
	cv2.rectangle(ui,(250,150),(300,200),(0,255,255),6)
	cv2.putText(ui,"C",(265,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
	
	cv2.rectangle(ui,(180,150),(230,200),(0,255,255),6)
	cv2.putText(ui,"B",(195,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)

	cv2.rectangle(ui,(110,150),(160,200),(0,255,255),6)
	cv2.putText(ui,"A",(125,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
	
	low_th=cv2.getTrackbarPos('low_th', 'thr')
	high_th=cv2.getTrackbarPos('high_th', 'thr')
#get kinect input__________________________________________________________________________
	disp = pretty_depth(freenect.sync_get_depth()[0])#input from kinect
    	orig = freenect.sync_get_video()[0]
    	orig = cv2.cvtColor(orig,cv2.COLOR_BGR2RGB) #to get RGB image, which we don't want
	cv2.flip(orig, 0, orig)#since we keep kinect upside-down
    	cv2.flip(orig, 1,orig)# thus correcting upside-down mirror effect
    	cv2.flip(disp, 0, disp)#since we keep kinect upside-down
	cv2.flip(disp, 1,disp)# thus correcting upside-down mirror effect
        #cv2.resize(orig,320,240,orig)
	thr=cv2.inRange(disp,low_th,high_th)
	thr=cv2.erode(thr, kernel, iterations=1)
	
	orig=orig[0:400,0:640]
	disp=disp[0:400,0:640]
	thr=thr[0:400,0:640]
	#thr = cv2.resize(thr, (0,0), fx=1.13, fy=1.12) #to superimpose absolute contour position on actual hand position (768/400=1.92)
	#cv2.rectangle(orig,(195,150),(220,180),(0,255,255),5)#fixed
	contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	cv2.drawContours(disp, contours, -1, 170, -1)
	cv2.drawContours(ui, contours, -1, (255,255,0), -1)
	for i in contours:
		x,y,w,h = cv2.boundingRect(i)
		cv2.rectangle(ui,(x,y),(x+w,y+h),(255,0,255),1)#contour unscaled location
		cv2.rectangle(orig,(x,y),(x+w,y+h),(0,0,255),5)#Kinect perception
		#cv2.rectangle(ui,(x,y),(x+w,y+h),(0,0,255),5)#Kinect perception of hand
		x_ui=(x*758)/640#random calib values
		w_ui=(w*1368)/640# not 1366; screen resolution changes to sq when projector is plugged
		y_ui=(y*758)/480#random calib values
		h_ui=(h*768)/480

		'''Note: Calibration values depend on exact Kinect position and angle :('''

		#cv2.rectangle(ui,(x_ui,y_ui),(x_ui+w_ui,y_ui+h_ui),(255,0,0),5)#approximated to hand location
		
		if(x>250 and x<300 and y>150 and y<200):
			cv2.putText(ui,"C",(300,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		if(x>180 and x<230 and y>150 and y<200):
			cv2.putText(ui,"B",(270,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		if(x>110 and x<160 and y>150 and y<200):
			cv2.putText(ui,"A",(240,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		if(x>320 and x<370 and y>150 and y<200):
			cv2.putText(ui,"D",(330,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		
		cv2.rectangle(disp,(x,y),(x+w,y+h),0,3)
	orig = cv2.resize(orig, (0,0), fx=0.25, fy=0.25) 
	disp = cv2.resize(disp, (0,0), fx=0.5, fy=0.5) 
	#thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	
	#ui = cv2.resize(ui, (0,0), fx=1.4, fy=1.60) 
	
	
#rectangular border (improved edge detection + closed contours)___________________________ 
	
#image binning (for distinct edges)________________________________________________________
    
    	#e=cv2.getTrackbarPos('erode', 'Video') 
    	
    	#disp = (disp/20)*20
    	#cv2.threshold(disp,230,255,cv2.THRESH_BINARY_INV,disp)
 	  

	
#finding contours__________________________________________________________________________
    	#contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	#cv2.drawContours(disp, contours, -1, (0, 0, 255), -1)
    #cv2.drawContours(orig, contours, -1, (0, 0, 255), -1)
	#inString="Input_"+str(count)+".jpg"
	#depString="Out_"+str(count)+".jpg"


	#cv2.imshow('thr',thr)			
#imshow outputs______________________________________________________________________   
    	#cv2.imshow('Input',orig)
	cv2.imshow('ui',ui)
	
	#print flag
	#cv2.destroyWindow('Navig')
	cv2.imshow('disparity', disp)
    	
	#cv2.imwrite(inString,orig)
	#cv2.imwrite(depString,disp)	

       	if(cv2.waitKey(10) & 0xFF == ord('b')):
        	break
