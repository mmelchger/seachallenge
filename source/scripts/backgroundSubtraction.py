import numpy as np
import cv2
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('video.avi')
fgbg1 = cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg2 = cv2.createBackgroundSubtractorMOG2()

#while(1):
#    ret, frame = cap.read()
#    fgmask = fgbg.apply(frame)
#    cv2.imshow('frame',fgmask)
#    k = cv2.waitKey(30) & 0xff
#    if k == 27:
#        break
#cap.release()
#cv2.destroyAllWindows()


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

downsampling = 30;
i = 0;
while(1):
    ret, frame = cap.read()
    if(i < downsampling):
        i = i + 1;
        continue;
    else:
        i = 0;
        
       
        fgmask = fgbg.apply(frame)
        
        fgmask1 = fgbg.apply(frame)
        fgmask2 = fgbg.apply(frame)
        fgmask3 = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        
        
        #fgmaskSum = fgmask1+fgmask2+fgmask3;
        
        
        kernel2 = np.ones((5,5),np.uint8)
       # erosion = cv2.erode(fgmaskSum,kernel2,iterations = 2)
       # dilation = cv2.dilate(erosion,kernel2,iterations = 2)
        
        closing = cv2.morphologyEx(fgmask1, cv2.MORPH_CLOSE, kernel2)
        #opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel2)
        
        #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        #closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel2)
        
        cv2.imshow('frame',fgmask1)
        cv2.imshow('frame2',frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()