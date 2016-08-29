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
#ui=cv2.imread("ui_paint.jpg")#global blank frame, will be painted
ui=cv2.imread("ui_blank2.jpg")
flag=0

count=0
x=0
y=0
w=0
h=0

xb=44#slider bar locations
yb=125

xg=74
yg=125

xr=104
yr=125

b=200
g=200
r=200
m=1#slope
c=0#init intercept
color=b,255,255
#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	#ui=cv2.imread("ui_paint.jpg")
	count=count+1
	#ui=cv2.imread("ui_blank.jpg")
	#ui=cv2.imread("ui_blank.jpg")
	#Scaling Ref rects_________________________________________
	cv2.rectangle(ui,(0,0),(110,480),(77,177,35),200)#ui color; so that panel values aren't smudged all over
	cv2.rectangle(ui,(0,0),(210,480),(0,0,0),2)#really thick rect sticks out of 110
	
	cv2.rectangle(ui,(0,0),(640,480),(0,0,0),2)#really thick rect sticks out of 110
	
	#blue slider
	cv2.rectangle(ui,(50,70),(60,325),(150,50,0),2)#blue slider bar
	
	cv2.rectangle(ui,(50,350),(60,360),(150,50,0),2)# blue -
	cv2.putText(ui,"-",(35,360),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,50,0),2)
	cv2.rectangle(ui,(50,330),(60,340),(150,50,0),2)# blue +
	cv2.putText(ui,"+",(35,340),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,50,0),2)

	#green slider
	cv2.rectangle(ui,(80,70),(90,325),(0,100,0),2)#green slider bar
	
	cv2.rectangle(ui,(80,350),(90,360),(0,100,0),2)# green -
	cv2.putText(ui,"-",(65,360),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,100,0),2)
	cv2.rectangle(ui,(80,330),(90,340),(0,100,0),2)# green +
	cv2.putText(ui,"+",(65,340),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,100,0),2)
	
	#red slider
	cv2.rectangle(ui,(110,70),(120,325),(0,0,150),2)#red slider bar
	
	cv2.rectangle(ui,(110,350),(120,360),(0,0,150),2)# red -
	cv2.putText(ui,"-",(95,360),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,150),2)
	cv2.rectangle(ui,(110,330),(120,340),(0,0,150),2)# red +
	cv2.putText(ui,"+",(95,340),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,150),2)



	
	
	

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
	cv2.rectangle(disp,(0,0),(210,480),(0,0,0),2)#slider bars on disp
	cv2.rectangle(disp,(50,70),(60,325),(150,50,0),2)#blue slider bar
	cv2.rectangle(disp,(80,70),(90,325),(0,100,0),2)#green slider bar
	cv2.rectangle(disp,(110,70),(120,325),(0,0,150),2)#red slider bar
	color=b,g,r#update color value
	for i in contours:
		x,y,w,h = cv2.boundingRect(i)
		if(x<180):
			#draw hand only if it's on panel
			#cv2.rectangle(ui,(x,y),(x+w,y+h),(255,0,255),1)#contour unscaled location
			cv2.line(ui,(x,y),(x+15,y),(75,100,200),4)
			cv2.line(ui,(x,y),(x,y+15),(75,100,200),4)
			cv2.line(ui,(x,y+15),(x+15,y),(75,100,200),4)
			#cv2.drawContours(ui, contours, -1, (255,255,0), -1)
		'''we may have hand prints on canvas if we use 2 hands together, hence a mouse pointer is drawn instead'''

		cv2.rectangle(orig,(x,y),(x+w,y+h),(0,0,255),5)#Kinect perception, not on ui
		if(x>210):
			cv2.circle(ui, (x,y), 3, color, 5)#brush out of panel
			cv2.circle(disp, (x,y), 3, (0,0,0), 5)#brush out of panel
		
		#button activators________________
		if(x>50 and x<60 and y>350 and y<360 and yb<=325 and yb>=70):# blue -
			yb=yb+2#as yb rises, slider falls
		if(x>50 and x<60 and y>330 and y<340 and yb<=325 and yb>=70):# blue +
			yb=yb-2#as yb falls, slider rises

		if(x>80 and x<90 and y>350 and y<360 and yg<=325 and yg>=70):# green -
			yg=yg+2#as yg rises, slider falls
		if(x>80 and x<90 and y>330 and y<340 and yg<=325 and yg>=70):# green +
			yg=yg-2#as yg falls, slider rises
		
		if(x>110 and x<120 and y>350 and y<360 and yr<=325 and yr>=70):# red -
			yr=yr+2#as yr rises, slider falls
		if(x>110 and x<120 and y>330 and y<340 and yr<=325 and yr>=70):# red +
			yr=yr-2#as yr falls, slider rises

		# Address corner cases__________________________________
		if(yb<70):
			yb=70
		if(yg<70):
			yg=70
		if(yr<70):
			yr=70
		if(yb>325):
			yb=325
		if(yg>325):
			yg=325
		if(yr>325):
			yr=325

		

 
		
		

		
		'''Note: Calibration values depend on exact Kinect position and angle :('''
	

		cv2.rectangle(disp,(x,y),(x+w,y+h),0,3)# on disparity

	#Pointers_____________________
	cv2.circle(ui, (xb,yb), 3, (150, 50, 0), 1)# this is our blue slider pointer
	cv2.line(ui,(xb-10,yb-10),(xb,yb),(150,50,0),4)
	cv2.line(ui,(xb-10,yb+10),(xb,yb),(150,50,0),4)
	cv2.line(ui,(xb-10,yb-10),(xb-10,yb+10),(150,50,0),4)

	cv2.circle(ui, (xg,yg), 3, (0, 100, 0), 1)# this is our green slider pointer
	cv2.line(ui,(xg-10,yg-10),(xg,yg),(0,100,0),4)
	cv2.line(ui,(xg-10,yg+10),(xg,yg),(0,100,0),4)
	cv2.line(ui,(xg-10,yg-10),(xg-10,yg+10),(0,100,0),4)

	cv2.circle(ui, (xr,yr), 3, (0, 0, 150), 1)# this is our red slider pointer
	cv2.line(ui,(xr-10,yr-10),(xr,yr),(0,0,150),4)
	cv2.line(ui,(xr-10,yr+10),(xr,yr),(0,0,150),4)
	cv2.line(ui,(xr-10,yr-10),(xr-10,yr+10),(0,0,150),4)


	b=325-yb
	g=325-yg
	r=325-yr
	cv2.rectangle(ui,(30,30),(140,50),color,25)#color ref rect
	
	
	orig = cv2.resize(orig, (0,0), fx=0.25, fy=0.25) 
	disp = cv2.resize(disp, (0,0), fx=0.5, fy=0.5) 
	#thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	thr = cv2.resize(thr, (0,0), fx=0.5, fy=0.5) 
	



	#cv2.imshow('thr',thr)			
#imshow outputs______________________________________________________________________   
    	#cv2.imshow('Input',orig)
	cv2.imshow('ui',ui)
	
	#print flag
	#cv2.destroyWindow('Navig')
	cv2.imshow('disparity', disp)
    	
	#cv2.imwrite(inString,orig)
	#cv2.imwrite(depString,disp)	
	#waitKey controls ball speed
       	if(cv2.waitKey(5) & 0xFF == ord('b')):
        	break
