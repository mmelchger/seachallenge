# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



#import sys
#sys.path.append('/usr/local/lib/python2.7/dist-packages/libais-0.17-py2.7-linux-x86_64.egg/ais')
import json 
import ais
import ais.stream
import json
import math

import geopy.distance

run = True; 

class TrackList:
    def __init__(self, mmsi):
       self.mmsi = mmsi;
       self.timeTable = {};
       self.lastTimeStampHr = -1;
       self.lastTimeStampMin = -1;       
       self.lastTimeStampSec = -1;
       self.lastX = -1;
       self.lastY = -1;
       self.lastSpeed = -1;
       
    def updateInteralValues(self, hour,minute,second,x,y,cog,sog):
        self.lastTimeStampHr = hour; 
        self.lastTimeStampMin = minute; 
        self.lastTimeStampSec = second; 
        self.lastX = x; 
        self.lastY = y; 
        self.lastSpeed = sog; 
    
    def normalizeGeoCoordinates(self,x, y):
        if(x > 180):
            x = 180 - x;
        elif(x < -180):
            x = x + 180;
        
        if(y > 90) : 
            y = 90 - (y%90);
        elif(y < -90):
            y = y+y%90;
        
        return (x,y);
    
    def timeBetweenPositions(self,xOld, yOld, xNew,yNew, hOld,minOld,secondsOld, speed):
        
        # print (str(xOld) + " , " + str(yOld) + " , " + str(xNew) + " , " + str(yNew))
        
        (xOld, yOld) = self.normalizeGeoCoordinates(xOld, yOld);
        (xNew, yNew) = self.normalizeGeoCoordinates(xNew,yNew);
            
        coordinatesBefore = (xOld, yOld);
        coordinatesNow = (xNew,yNew);
        
        distanceSinceLast = geopy.distance.vincenty(coordinatesBefore, coordinatesNow).nautical;
        secondsSinceLast = 1;
        if(not speed == 0):
            secondsSinceLast = (distanceSinceLast / speed)*3600;
        
        seconds = int(secondsOld+ secondsSinceLast); 
        minutes = int(minOld + (seconds - seconds%60)/60);
        hours = int((hOld + (seconds - seconds%3600)/3600));
        seconds = ((secondsOld+secondsSinceLast)%60);
        time = (int(hours), int(minutes), int(seconds))

        return time; 
        
    
    def addCompleteEntry(self, hour, minute, x, y, cog, sog):
        second = 0; 
        
        # if(self.lastTimeStampHr > 10 or self.lastTimeStampHr ==23):
        # if(self.lastTimeStampHr - 12 == hour):
        #     hour = hour + 12
        
        time = self.timeBetweenPositions(self.lastX, self.lastY, x,y,self.lastTimeStampHr,self.lastTimeStampMin, self.lastTimeStampSec,self.lastSpeed);
        self.timeTable[(time[0],time[1], time[2])] = (x,y,cog,sog);
        self.updateInteralValues(hour,minute, second, x,y,cog,sog); 
        
        
    def addEntryWithoutTime(self, x, y, cog, sog):
        
        (hour, minute,second) = self.timeBetweenPositions(self.lastX, self.lastY, x,y,self.lastTimeStampHr,self.lastTimeStampMin, self.lastTimeStampSec,self.lastSpeed);
        self.timeTable[(hour,minute,second)] = (x,y,cog,sog);                
        self.updateInteralValues(hour,minute, second, x,y,cog,sog); 
        
    
def processMessage(jsonDecoded, trackList):
    time = ""
    timeNr=0; 
    if ("utc_hour" in jsonDecoded ):
        hr =jsonDecoded["utc_hour"];
        if(timeNr>10):
            if(timeNr == 23):
                if(hr == 24):
                    hr = 0;
            else:
                if(hr<10):
                    hr = hr + 12;
        timeNr = hr;
        minute = jsonDecoded["utc_min"]; 
        time = str(hr) + "," + str(minute)
        
        
    if (("mmsi" in jsonDecoded) and ("sog" in jsonDecoded) and ("x" in jsonDecoded) and ("y" in jsonDecoded)):
        mmsi = jsonDecoded["mmsi"];
        x = jsonDecoded["x"]; 
        y = jsonDecoded["y"]; 
        sog = jsonDecoded["sog"]
        if(not mmsi in trackList):
            trackList[mmsi] = TrackList(mmsi)
        
        if(not "utc_hour" in jsonDecoded):
            trackList[mmsi].addEntryWithoutTime(x, y, 0, sog);
        else:
            trackList[mmsi].addCompleteEntry(hr,minute,x, y, 0, sog);
            
        outstream = "";
        time = str(trackList[mmsi].lastTimeStampHr) +","+ str(trackList[mmsi].lastTimeStampMin) +","+ str(trackList[mmsi].lastTimeStampSec);
        # if ("utc_hour" in jsonDecoded ):
        #     outstream = str(jsonDecoded["utc_hour"]) + "," + str(jsonDecoded["utc_min"])
        outstream = time + "," + str( trackList[mmsi].lastSpeed )+"," + str(sog)
        
        with open("./aissortedbyship/" + str(jsonDecoded["mmsi"])+".txt", 'a') as outfile:
            outfile.write(outstream+"\n")

trackList = {};
        
if(run):
    with open("/home/m/aislog_20190302.txt") as f:
        dS = ais.stream.decode(f)
        for msg in dS:
            processMessage(msg,trackList);
