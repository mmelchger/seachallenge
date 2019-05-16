# -*- coding: utf-8 -*-
"""
Displaying text and draw on images
"""

import numpy as np
import cv2

class RectangleOverlay: 

    def __init__(self):
        pass
    
    def setRectangle(self, xStart, yStart, xEnd, yEnd):
        self.xStart = xStart; 
        self.xEnd = xEnd; 
        self.yStart = yStart; 
        self.yEnd = yEnd; 
    
    def setColor(self, color):
        self.color = color;
        
    def setThickness(self, thickness):
        self.thickness = thickness;
        
    def setName(self, name):
        self.name = name;
    
    def setSog(self, sog):
        self.sog = sog; 
    
    def setCog(self, cog):
        self.cog = cog; 
    
    def setHdg(self, hdg):
        self.hdg = hdg;
    
    def addToImage(self, img, highlight=False):
        lineThickness = 1;
        if(highlight == True):
            lineThickness = 3;
        
        cv2.rectangle(img,(self.xStart,self.yStart),(self.xEnd,self.yEnd),self.color,lineThickness)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Ship name',(self.xStart,self.yEnd+30), font, 0.8,self.color,1,cv2.LINE_AA)
        cv2.putText(img,'HDG '+'112',(self.xStart,self.yEnd+60), font, 0.8,self.color,1,cv2.LINE_AA)
        cv2.putText(img,'SOG '+'15KN',(self.xStart,self.yEnd+90), font, 0.8,self.color,1,cv2.LINE_AA)
        cv2.putText(img,'CPA '+'0.1NM',(self.xStart,self.yEnd+120), font, 0.8,self.color,1,cv2.LINE_AA)
        
class OverlayManager:
    def __init__(self, overlayTypeName):        
        self.overlayTypeName = overlayTypeName;
        self.overlays =[];
        self.heightY = 128;
        self.widthX = 128;
        
    def setWidthX(self, widthX):
        self.widthX = widthX; 
        
    def setHeightY(self, heightY):
        self.heightY = heightY; 
     
    
    def positionOccupied(self,x,y):
        result = (False,None);
        for i in range(len(self.overlays)):
            print(str(i))
            overlay = self.overlays[i];
            if((x>=overlay.xStart and x<=overlay.xEnd)):
                if((y>=overlay.yStart and y<=overlay.yEnd)):
                    result = (True,i);
        return result; 
            
    
    def addOverlay(self, x,y):
        
        xStart = round(x-self.widthX/2);
        xEnd = xStart + self.widthX; 
        
        yStart = round(y-self.heightY/2);
        yEnd = yStart + self.heightY; 
        
        overlay = RectangleOverlay();
        overlay.setRectangle(xStart, yStart, xEnd, yEnd);
        overlay.setCog(123);
        overlay.setSog(14);
        overlay.setHdg(321);
        overlay.setColor((int(np.mod(x,256)),int(np.mod(y,256)),int(np.mod(y*x,256))));
        overlay.setThickness(50);
        overlay.addToImage(img);

        self.overlays.append(overlay);

    def highlightOverlay(self,i):
        overlay = self.overlays[i];
        
        
    def handleClick(self,x,y):
        result = self.positionOccupied(x,y);
        if(result[0] == True):
            print("Exists")
            #self.highlightOverlay(result[1]);
        else:
            self.addOverlay(x,y);
        
    def handleHover(self,x,y):
        pass
    
    def update(self, img):
        for i in range(len(self.overlays)):
            overlay = self.overlays[i];
            overlay.addToImage(img); 
    
manager = OverlayManager("Ships"); 

def updateImage(img):
    img = np.zeros((540,960,3), np.uint8);
    manager.update(img); 
    cv2.imshow('image',img)
    
def clearImage(img):
    img = np.zeros((540,960,3), np.uint8);
    cv2.imshow('image',img)

def mouseHandler(event,x,y,flags,param):
    global mouseX,mouseY

    if event == cv2.EVENT_MOUSEMOVE :
        pass
    elif event == cv2.EVENT_LBUTTONDOWN :
        print("EVENT_LBUTTONDOWN [" + str(x) + " , " + str(y) + "]")
        manager.handleClick(x,y);
        updateImage(img); 
        
    elif event == cv2.EVENT_RBUTTONDOWN :
        pass
    elif event == cv2.EVENT_MBUTTONDOWN :
        pass
    elif event == cv2.EVENT_LBUTTONUP :
        print("EVENT_LBUTTONUP [" + str(x) + " , " + str(y) + "]")
        clearImage(img);
    elif event == cv2.EVENT_RBUTTONUP :
        pass
    elif event == cv2.EVENT_MBUTTONUP :
        pass
    elif event == cv2.EVENT_LBUTTONDBLCLK :
        pass
    elif event == cv2.EVENT_RBUTTONDBLCLK :
        pass
    elif event == cv2.EVENT_MBUTTONDBLCLK :
        pass
    elif event == cv2.EVENT_MOUSEWHEEL :
        pass
    elif event == cv2.EVENT_MOUSEHWHEEL :
        pass
    else: 
        pass
    
    updateImage(img);
        
         
# Create a black image
img = np.zeros((540,960,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
#cv2.line(img,(0,0),(511,511),(255,0,0),5)

#cv2.circle(img,(447,63), 63, (0,0,255), -1)
#cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)

#pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
#pts = pts.reshape((-1,1,2))
#cv2.polylines(img,[pts],True,(0,255,255))

cv2.namedWindow('image')
cv2.setMouseCallback('image',mouseHandler)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()