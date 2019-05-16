# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 20:14:46 2019

@author: m
"""
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleEcho(WebSocket):
    def __init__(self):
        self.gobalData = [
            [54.322631, 10.145531]
            [54.330639, 10.161324]
            [54.342149, 10.165958]
            [54.352155, 10.167847]
            [54.365958, 10.170937]
            [54.382257, 10.187588]
            [54.403545, 10.204582]
            [54.433513, 10.201321]
            [54.438302, 10.251789]
            ]
        self.globalIndex = 0

    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')
        
    def sendPositions(self):
        while (True):
            self.globalIndex = self.globalIndex + 1
            self.globalIndex = self.globalIndex%9
            self.sendMessage(globalData(gobalData))


def main():
    server = SimpleWebSocketServer('', 8000, SimpleEcho)
    server.serveforever()


if __name__ == '__main__':
    main()