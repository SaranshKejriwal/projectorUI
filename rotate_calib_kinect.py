import freenect
import cv2
import numpy as np
import math#for tan inverse
#from functions import *

def nothing(x):
    pass
def rotateImage(image, angle):
   (h, w) = image.shape[:2]
   center = (w / 2, h / 2)
   M = cv2.getRotationMatrix2D(center,angle,1.0)
   rotated_image = cv2.warpAffine(image, M, (w,h))
   return rotated_image
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
#ui=cv2.imread("ui_paint.jpg")#global blank frame, will be painted
ui=cv2.imread("ui_paint.jpg")
pic=cv2.imread("Genos.png")
pic = cv2.resize(pic, (0,0), fx=0.25, fy=0.25) 


pic_size=366,366,3#366 is image diagonal length
pic_sq=np.zeros(pic_size,dtype=np.uint8)
pic_sq[93:272,23:342]=pic# put Genos on a square frame

#ui=blank#clear the painting from last run

#cv2.imwrite("ui_paint.jpg",ui)
paint_flag=0#to toggle in and out of paint mode
count=0
x=0
y=0
w=0
h=0#to get crosshair out of loop

xl=170
yl=170# top left rect pt
xr=330#
yr=330# bottom right rect pt
sx=xr-xl#sides
sy=yr-yl
xm=320
ym=200#ellipse center(fixed)
axes=(100,50)#initialize
angle=90
#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	#ui=cv2.imread("ui_paint.jpg")
	count=count+1
	ui=cv2.imread("ui_blank2.jpg")
	#ui=cv2.imread("ui_blank.jpg")
	#Scaling Ref rects_________________________________________
	cv2.rectangle(ui,(0,0),(640,480),(155,255,255),2)
	cv2.rectangle(ui,(0,0),(1366,768),(155,255,255),2)
	cv2.circle(ui,(320,200), 5, (150, 50, 0), 5)# ellipse centre
	

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
		cx=x+w/2
		cy=y+h/2#hand center
		cv2.rectangle(orig,(x,y),(x+w,y+h),(0,0,255),5)#Kinect perception, not on ui
		cv2.rectangle(ui,(x,y),(x+w,y+h),(255,0,255),1)#contour unscaled location
		cv2.line(ui,(320,200),(cx,cy),(255,0,0),2)

		if(cx>320 and cy<200):#270-360
			angle=360-math.degrees(math.atan(float(200-cy)/float(cx-320)))
			axes=(cx-320,(cx-320)/3)
		if(cx>320 and cy>200):#0-90
			angle=math.degrees(math.atan(float(cy-200)/float(cx-320)))
			axes=(cx-320,(cx-320)/3)
		if(cx<320 and cy<200):#180-270
			angle=math.degrees(math.atan(float(cy-200)/float(cx-320)))
			axes=(320-cx,(320-cx)/3)
		if(cx<320 and cy>200):#90-180
			angle=math.degrees(math.atan(float(cy-200)/float(cx-320)))
			axes=(320-cx,(320-cx)/3)


		if(cx<350 and cx>320):
			axes=(cx-320,40)#prevent really small ellipses
		if(cx<320 and cx>290):
			axes=(320-cx,40)#prevent really small ellipses
		'''if(x<xm-50 and x>xl-50 and y>yl-50 and y<ym-50):#top left resize
			xl=x #determine top left zooming of rect
			yl=y
			
			#xm=(xl+xr)/2# recalc mid pt. since rect is reshaped
			#ym=(yl+yr)/2
			sx=xr-xl#sides recalc as rect is reshaped
			sy=yr-yl
		if(x>xm+50 and x<xr+50 and y<yr+50 and y>ym+50):#bottom left resize
			xr=x #determine bottom right zooming of rect
			yr=y
			#xm=(xl+xr)/2# recalc mid pt. since rect is reshaped
			#ym=(yl+yr)/2
			sx=xr-xl#sides recalc as rect is reshaped
			sy=yr-yl
		if(x<xm and x>xl-50 and y>ym and y<yr+50):#when hand is in a 30X30 dist from centre
			xl=x#moving rect around, hence dims don't change
			yr=y
			#xr=xl+sx#sides don't change if rect is moved
			#yl=yr-sy
			xm=(xl+xr)/2# recalc mid pt. since rect is moved
			ym=(yl+yr)/2
		if(x>xm and x<xr+50 and y<ym and y>yl-50):#when hand is in a 30X30 dist from centre
			#try rotate on top left move
			xr=x#moving rect around, hence dims don't change
			yl=y
			xl=xr-sx#sides don't change if rect is moved
			yr=yl+sy
			#xm=(xl+xr)/2# recalc mid pt. since rect is moved
			#ym=(yl+yr)/2

		if(xr<xl+sx):#address boundary conditions
			xr=xl+sx
		if(yr<yl+sy):#address boundary conditions, if image is moved to (x,0)
			yr=yl+sy
		if(yl<10):
			yl=10
			yr=yl+sy# do not resize while moving upwards (no img crushing)
			#ym=(yl+yr)/2
		if(yr>470):
			yr=470
			yl=yr-sy# do not resize while moving upwards (no img crushing)
			#ym=(yl+yr)/2
		if(xr>640):
			xr=640
			xl=xr-sy# do not resize while moving upwards (no img crushing)
			xm=(xl+xr)/2'''


		'''Note- Resize and Move ops can't be simultaneous'''

		#cv2.circle(ui, (x,y), 2, (25, 25, 205), 2)
		#cv2.imwrite("ui_paint.jpg",ui)#write back painting to UI in each frame, to be re-read
		'''Note: Imwriting to jpg causes slight colour fading due to encoding change from tiff to jpg'''
		
		'''Note: Calibration values depend on exact Kinect position and angle :('''

		#cv2.rectangle(ui,(x_ui,y_ui),(x_ui+w_ui,y_ui+h_ui),(255,0,0),5)#actual hand location
		#cv2.rectangle(ui,(x,y),(x+w,y+h),(255,0,255),1)#contour unscaled location
		

		cv2.rectangle(disp,(x,y),(x+w,y+h),0,3)
	#cv2.circle(ui, (x0,y0), 10, (150, 50, 0), 20)# this is our ball
	#cv2.rectangle(ui,(xl,yl),(xr,yr),(0,50,0),5)#result rect
	
	#pic_size=366,366,3#366 is image diagonal length
	#pic_rot=np.zeros(pic_size,dtype=np.uint8)
	#pic_rot[97:272,144:461]=pic
	pic_rot=rotateImage(pic_sq, 360-angle)
	ui[17:383,137:503]=pic_rot
	cv2.ellipse(ui,(320,200),axes,angle,0,360,(255,0,0),5)#result ellipse
	#cv2.ellipse(ui,(320,200),(150,50),angle,0,360,(255,0,0),5)#fixed size ellipse
	#cv2.ellipse(ui,(320,200),(150,50),135,0,360,(255,0,0),5)#ref ellipse
	#cv2.putText(ui,"A",(xl,yl),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)
	#cv2.putText(ui,"B",(xr,yr),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)
	'''cv2.rectangle(disp,(xl,yl),(xr,yr),(0,50,0),5)#result rect
	cv2.putText(disp,"resize",(xl,yl),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)
	cv2.putText(disp,"resize",(xr,yr),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)#locate rect vertices
	cv2.putText(disp,"move",(xr,yl),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)#locate rect vertices
	cv2.putText(disp,"move",(xl,yr),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)#locate rect vertices
	cv2.putText(disp,"C",(xm,ym),cv2.FONT_HERSHEY_TRIPLEX,1,(0,50,0),2)#locate rect vertices


	pic_scale_x=(float(xr-xl)/pic_w)#get the scaling factor of zoomed pic, to fit in rect
	pic_scale_y=(float(yr-yl)/pic_h)#/pic_h#get the scaling factor of zoomed pic, to fit in rect
	#print "height scale="+str(pic_scale_x)
	#print "width scale="+str(pic_scale_y)
	result_pic = cv2.resize(pic, (0,0), fx=pic_scale_x, fy=pic_scale_y)#resize img acc to result rect
	ui[yl:yr,xl:xr]=result_pic#paste pic on ui, size should be same'''
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
	thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	
	ui = cv2.resize(ui, (0,0), fx=1.4, fy=1.60) 
	#imshow outputs______________________________________________________________________   
    	#cv2.imshow('Input',orig)
	cv2.imshow('ui',ui)
	
	#print flag
	#cv2.destroyWindow('Navig')
	cv2.imshow('disparity', disp)
    	
       	if(cv2.waitKey(5) & 0xFF == ord('b')):
        	break
