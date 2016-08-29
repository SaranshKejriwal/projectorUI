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

cv2.namedWindow('Input')
cv2.moveWindow('Input',0,600)
cv2.createTrackbar('low_th', 'thr', 220, 255, nothing)
cv2.createTrackbar('high_th', 'thr', 223, 255, nothing)
#cv2.namedWindow('Win')
kernel = np.ones((5, 5), np.uint8)


print('Press \'b\' in window to stop')
#ui=cv2.imread("ui_paint.jpg")#global blank frame, will be painted
ui=cv2.imread("ui_blank.jpg")
#ui=blank#clear the painting from last run

#cv2.imwrite("ui_paint.jpg",ui)
paint_flag=0#to toggle in and out of paint mode
count=0
x=0
y=0
w=0
h=0#to get crosshair out of loop

x0=200
y0=120# ball position ; Simulating a Kalman filter
xb=200
xg=200
xr=200
m=1#slope
c=0#init intercept
#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	#ui=cv2.imread("ui_paint.jpg")
	count=count+1
	ui=cv2.imread("ui_blank.jpg")
	#ui=cv2.imread("ui_blank.jpg")
	#Scaling Ref rects_________________________________________
	cv2.rectangle(ui,(0,0),(640,480),(155,255,255),2)
	cv2.rectangle(ui,(0,0),(1366,768),(155,255,255),2)
	cv2.rectangle(ui,(100,110),(500,118),(155,50,0),2)#blue slider bar
	cv2.rectangle(ui,(520,110),(530,118),(150,50,0),2)# blue -
	cv2.putText(ui,"-",(518,108),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,50,0),1)


	#UI buttons_____________________________________________________
	cv2.rectangle(ui,(320,150),(370,200),(0,255,255),6)
	cv2.putText(ui,"+",(335,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
	cv2.rectangle(ui,(180,150),(230,200),(0,255,255),6)
	cv2.putText(ui,"-",(195,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
	'''cv2.rectangle(ui,(250,150),(320,200),(0,255,255),6)
	cv2.putText(ui,"Off",(255,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
	
	cv2.rectangle(ui,(180,150),(230,200),(0,255,255),4)
	cv2.putText(ui,"On",(185,185),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)

	#cv2.rectangle(ui,(50,150),(140,200),(0,255,255),4)
	cv2.putText(ui,"Paint",(55,185),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,255),3)'''
	
	

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
	#cv2.rectangle(orig,(195,150),(220,180),(0,255,255),5)#fixed
	contours, hierarchy = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	cv2.drawContours(disp, contours, -1, 170, -1)
	cv2.drawContours(ui, contours, -1, (255,255,0), -1)
	for i in contours:
		x,y,w,h = cv2.boundingRect(i)
		cv2.rectangle(ui,(x,y),(x+w,y+h),(255,0,255),1)#contour unscaled location
		cv2.rectangle(orig,(x,y),(x+w,y+h),(0,0,255),5)#Kinect perception, not on ui

		if(x>320 and x<370 and y>150 and y<200):
			#cv2.putText(ui,"+",(330,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
			x0=x0+2

		if(x>180 and x<230 and y>150 and y<200):
			#cv2.putText(ui,"-",(270,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
			x0=x0-2

		'''if(x<x0):
			x0=x0-1
			if(y>y0 and x!=x0):
				m=((y-y0)/(x0-x))
			if(y<y0 and x!=x0):
				m=((y0-y)/(x0-x))
			if(y==y0 or x==x0):
				pass
			c=y-m*x
			y0=m*x0+c
		if(x>x0):
			x0=x0+1
			if(y<y0 and x!=x0):
				m=((y-y0)/(x0-x))
			if(y>y0 and x!=x0):
				m=((y0-y)/(x0-x))
			if(y==y0 or x==x0):
				pass
			c=y-m*x
			y0=m*x0+c
			#y0=((y0-y)/(x0-x))*(x0+x)-y
		if(x==x0 or y==y0):
			pass'''
		

		#cv2.circle(ui, (x,y), 2, (25, 25, 205), 2)
		#cv2.imwrite("ui_paint.jpg",ui)#write back painting to UI in each frame, to be re-read
		'''Note: Imwriting to jpg causes slight colour fading due to encoding change from tiff to jpg'''
		#cv2.circle(ui, (x,y), 3, (0, 0, 0), 3)# I hope this has no trail
		x_ui=(x*908)/640#random calib values
		w_ui=(w*968)/640# not 1366; screen resolution changes to sq when projector is plugged
		y_ui=(y*708)/480#random calib values
		h_ui=(h*768)/480

		'''Note: Calibration values depend on exact Kinect position and angle :('''

		#cv2.rectangle(ui,(x_ui,y_ui),(x_ui+w_ui,y_ui+h_ui),(255,0,0),5)#actual hand location
		#cv2.rectangle(ui,(x,y),(x+w,y+h),(255,0,255),1)#contour unscaled location
		'''if(x>50 and x<140 and y>150 and y<200 and paint_flag==0):
			cv2.putText(ui,"On",(155,185),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,105,0),3)
			paint_flag=1
		if(x>50 and x<140 and y>150 and y<200 and paint_flag==1):
			cv2.putText(ui,"Off",(155,185),cv2.FONT_HERSHEY_TRIPLEX,1.5,(0,0,255),3)
			paint_flag=0'''
		#if(x>180 and x<230 and y>150 and y<200):
			#cv2.putText(ui,"B",(270,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		#if(x>110 and x<160 and y>150 and y<200):
			#cv2.putText(ui,"A",(240,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		#if(x>320 and x<370 and y>150 and y<200):
			#cv2.putText(ui,"D",(330,80),cv2.FONT_HERSHEY_TRIPLEX,1.5,(255,255,255),3)
		#if(x>60 and x<90 and y>170 and y<200):
			#cv2.putText(ui,":)",(430,80),cv2.FONT_HERSHEY_TRIPLEX,2,(255,255,255),2)

		cv2.rectangle(disp,(x,y),(x+w,y+h),0,3)
	cv2.circle(ui, (x0,y0), 3, (150, 50, 0), 1)# this is our slider pointer
	cv2.line(ui,(x0-10,y0+10),(x0,y0),(150,50,0),7)
	cv2.line(ui,(x0+10,y0+10),(x0,y0),(150,50,0),7)
	cv2.line(ui,(x0-10,y0+10),(x0+10,y0+10),(150,50,0),7)
	'''cv2.line(ui,(x,y-5),(x,y-10),(0,0,0),2)#crosshair design
	cv2.line(ui,(x,y+5),(x,y+10),(0,0,0),2)
	cv2.line(ui,(x+5,y),(x+10,y),(0,0,0),2)
	cv2.line(ui,(x-5,y),(x-10,y),(0,0,0),2)'''

	'''cv2.circle(disp, (x,y), 4, (0, 0, 0), 2)# I hope this has no trail
	cv2.line(disp,(x,y-5),(x,y-10),(0,0,0),2)#crosshair design
	cv2.line(disp,(x,y+5),(x,y+10),(0,0,0),2)
	cv2.line(disp,(x+5,y),(x+10,y),(0,0,0),2)
	cv2.line(disp,(x-5,y),(x-10,y),(0,0,0),2)'''

	'''doesn't leave trail, but only 1 crosshair is drawn'''
	orig = cv2.resize(orig, (0,0), fx=0.25, fy=0.25) 
	disp = cv2.resize(disp, (0,0), fx=0.5, fy=0.5) 
	#thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	
	



	#cv2.imshow('thr',thr)			
#imshow outputs______________________________________________________________________   
    	cv2.imshow('Input',orig)
	cv2.imshow('ui',ui)
	
	#print flag
	#cv2.destroyWindow('Navig')
	cv2.imshow('disparity', disp)
    	
	#cv2.imwrite(inString,orig)
	#cv2.imwrite(depString,disp)	
	#waitKey controls ball speed
       	if(cv2.waitKey(5) & 0xFF == ord('b')):
        	break
