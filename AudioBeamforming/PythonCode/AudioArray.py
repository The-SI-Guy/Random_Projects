# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:33:02 2020

@author: the-SI-Guy
Microphone Array Class:
setPhases sets the phase values to user chosen values
CalcBeamSteeringPhases calculates the phase weights necessary to steer to an angle
AFaz calculates the Array factor in the azimuthal direction for uniform phase weights
AFel calculates the Array factor in the elevation direction for uniform phase weights
AFazArbitrary calculates the Array factor in the azimuthal direction for arbitrary phase weights
AFelArbitrary calculates the Array factor in the elevation direction for arbitrary phase weights
plotAF plots the AF for a given Az and El Array Factor value
polarPlotAF polar plot of above
dispArray shows the array geometry
AddRandPhaseError adds random phase error (in degrees) to the phase weights
"""


import numpy as np
import matplotlib.pyplot as plt
import random

class Array:
    Freq=np.NaN
    xElements = np.NaN
    yElements = np.NaN
    xSpacing = np.NaN
    ySpacing = np.NaN
    phases = np.NaN
    Baz = np.NaN
    Bel = np.NaN
    c = 343
    def __init__(self,Freq,xElements,yElements,xSpacing,ySpacing):
        self.Freq = Freq
        self.xElements = xElements
        self.yElements = yElements
        self.xSpacing = xSpacing
        self.ySpacing = ySpacing
    
    
    def CalcBeamSteeringPhases(self,theta=0,phi=0):
        assert (theta >= -90 and theta <= 90)
        assert (phi >= -90 and phi <= 90)
        self.phases = np.zeros((self.xElements,self.yElements))
        self.Baz = (2*np.pi*self.xSpacing/self.lamda)*np.sin((np.pi/180)*theta) # Azimuthal
        self.Bel = (2*np.pi*self.ySpacing/self.lamda)*np.sin((np.pi/180)*phi)
        for i in range(self.xElements):
            for j in range(self.yElements):
                self.phases[i][j] = i*self.Baz+j*self.Bel
                while self.phases[i][j]<0:
                    self.phases[i][j]+=2*np.pi
                if self.phases[i][j]>2*np.pi:
                    self.phases[i][j]%=2*np.pi
    def setPhases(self,phasesAz=0,phasesEl=0):
        if phasesAz==0:
            phasesAz = np.zeros(self.yElements)
        if phasesEl==0:
            phasesEl = np.zeros(self.xElements)
        self.phases = np.zeros((self.xElements,self.yElements))
        for i in range(self.xElements):
            for j in range(self.yElements):
                self.phases[i][j] = (np.pi/180)*phasesAz[i]+(np.pi/180)*phasesEl[j]
                
    def AFaz(self): ### uniform phase
        theta = np.linspace(-np.pi/2,np.pi/2,1001)
        num =  np.sin(self.xElements*((np.pi*self.xSpacing/self.lamda)*np.sin(theta)-self.Baz/2))
        den = self.xElements*np.sin((np.pi*self.xSpacing/self.lamda)*np.sin(theta)-self.Baz/2)
        return 10*np.log10((num/den)**2)
    
    def AFel(self): ### uniform phase
        theta = np.linspace(-np.pi/2,np.pi/2,1001)
        num =  np.sin(self.yElements*((np.pi*self.ySpacing/self.lamda)*np.sin(theta)-self.Bel/2))
        den = self.yElements*np.sin((np.pi*self.ySpacing/self.lamda)*np.sin(theta)-self.Bel/2)
        return 10*np.log10((num/den)**2)
    
    def AFazArbitrary(self):
        theta = np.linspace(0,np.pi,1001)
        AF = 0
        for i in range(self.xElements):
            if i==0:
                AF+=1
            else:
                AF+=np.exp(1j*i*(self.k*self.xSpacing*np.cos(theta)+(self.phases[i][0]-self.phases[i-1][0])))
        return 20*np.log10((1/self.xElements)*abs(AF))
   
    def AFelArbitrary(self):
        theta = np.linspace(0,np.pi,1001)
        AF = 0
        for i in range(self.yElements):
            if i==0:
                AF+=1
            else:
                AF+=np.exp(1j*i*(self.k*self.ySpacing*np.cos(theta)+(self.phases[0][i]-self.phases[0][i-1])))
        return 20*np.log10((1/self.yElements)*abs(AF))
    
    def plotAF(self,AFaz,AFel=0):
        theta = np.linspace(-90,90,1001)
        plt.figure()
        plt.plot(theta,AFaz,label="Azimuthal")
        plt.axis([-90,90,-40,1])
        plt.grid('on')
        plt.xlabel("Theta (Degrees)")
        plt.ylabel("Normalized Amplitude (dB)")
        #plt.plot(theta,AFel,label="Elevation")
        #plt.legend(loc='upper right')
        plt.title("Normalized Array Factor dx=.3,F0=200,N=8")
    def polarPlotAF(self,AFaz,AFel=0):
        theta = np.linspace(-np.pi/2,np.pi/2,1001)
        plt.polar(theta,AFaz,label="Azimuthal")
        plt.axis([-np.pi/2,np.pi/2,-80,0])
        plt.xlabel("Theta (Degrees)")
        plt.ylabel("Normalized Amplitude (dB)")
        #plt.polar(theta,AFel,label="Elevation")
        #plt.legend(loc='upper right')
        
    def dispArray(self):
        plt.figure()
        for i in range(self.xElements):
            for j in range(self.yElements):
                plt.plot((i)*self.xSpacing*1e3,(j)*self.ySpacing*1e3,'b*')
        plt.xlabel("xLocation (mm)")
        plt.ylabel("yLocation (mm)")
        plt.title("Microphone Locations")
        
    def AddRandPhaseError(self,AvgError=5):
        AvgError = (np.pi/180)*AvgError
        for i in range(self.xElements):
            for j in range(self.yElements):
                self.phases[i][j] = self.phases[i][j]+(random.randint(-100,100)/100)*AvgError
    

    @property
    def lamda(self):
        return self.c/self.Freq
    @property
    def k(self):
        return 2*np.pi/self.lamda
        
MicArray = Array(200,8,1,.3,0)
MicArray.CalcBeamSteeringPhases(60,0)
Az=MicArray.AFazArbitrary()
MicArray.plotAF(Az)
MicArray.polarPlotAF(Az)
MicArray.dispArray()
L = MicArray
