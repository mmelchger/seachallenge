# -*- coding: utf-8 -*-
"""
Displaying text and draw on images
"""

import numpy as np
import cv2

def mouseHandler(event,x,y,flags,param):
    global mouseX,mouseY;

    mouseX = x; 
    mouseY = y; 

    if event == cv2.EVENT_MOUSEMOVE :
        pass
    elif event == cv2.EVENT_LBUTTONDOWN :
        print("EVENT_LBUTTONDOWN")
        cv2.rectangle(frame,(x,y),(x+64,y+64),(0,0,255),1)
        cv2.imshow('frame',frame)
        cv2.waitKey(100)
        
    elif event == cv2.EVENT_RBUTTONDOWN :
        pass
    elif event == cv2.EVENT_MBUTTONDOWN :
        pass
    elif event == cv2.EVENT_LBUTTONUP :
        pass
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
    
#    def addToImage(self, img, highlight=False):
#        lineThickness = 1;
#        if(highlight == True):
#            lineThickness = 3;
#        
#        cv2.rectangle(img,(self.xStart,self.yStart),(self.xEnd,self.yEnd),self.color,lineThickness)
#        font = cv2.FONT_HERSHEY_SIMPLEX
#        cv2.putText(img,'Ship name',(self.xStart,self.yEnd+30), font, 0.8,self.color,1,cv2.LINE_AA)
#        cv2.putText(img,'HDG '+'112',(self.xStart,self.yEnd+60), font, 0.8,self.color,1,cv2.LINE_AA)
#        cv2.putText(img,'SOG '+'15KN',(self.xStart,self.yEnd+90), font, 0.8,self.color,1,cv2.LINE_AA)
#        cv2.putText(img,'CPA '+'0.1NM',(self.xStart,self.yEnd+120), font, 0.8,self.color,1,cv2.LINE_AA)
        
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
#        overlay.addToImage(img);

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


cap = cv2.VideoCapture(0)
manager = OverlayManager("ships");
manager.addOverlay(300,300);
manager.addOverlay(200,200);
manager.addOverlay(100,100);


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
        
    # Display the resulting frame
    for item in manager.overlays:
        cv2.rectangle(frame,(item.xStart,item.yStart),(item.xEnd,item.yEnd),item.color,2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Ship name',(item.xStart,item.yEnd+20), font, 0.5,item.color,1,cv2.LINE_AA)
        cv2.putText(frame,'HDG '+'112',(item.xStart,item.yEnd+40), font, 0.5,item.color,1,cv2.LINE_AA)
        cv2.putText(frame,'SOG '+'15KN',(item.xStart,item.yEnd+60), font, 0.5,item.color,1,cv2.LINE_AA)
        cv2.putText(frame,'CPA '+'0.1NM',(item.xStart,item.yEnd+80), font, 0.5,item.color,1,cv2.LINE_AA)
        
        item.xStart = item.xStart + 1;
        item.xEnd = item.xEnd + 1;
    
    cv2.imshow('frame',frame)
    cv2.setMouseCallback('frame',mouseHandler)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()