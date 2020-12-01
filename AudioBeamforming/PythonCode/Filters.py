# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:43:37 2020
FIR Filter Coefficient Calculator
@author: The-SI-Guy
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def calcFilterCoeff(delay,Fs,fc): 
    coeff = np.zeros(256)
    print("The delay is "+str(delay))
    nTaps = int(round(delay*2*Fs+1)) # Integer 
    print("The number of Taps are "+str(nTaps))
    coeff[0:nTaps] = signal.firwin(nTaps,fc,fs=Fs) #
    return coeff

def calcDelay(dx,v,steerAngle):
    delay = dx*np.sin(steerAngle)/v
    return delay

def getGroupDelays(N,steerAngle,v,dx):
    delays = np.ones(N)
    delays = delays * np.arange(0,N,1) * dx
    for i in range(N):
        delays[i] = calcDelay(delays[i],v,steerAngle)
    for i in range(N):
        delays[i] -= min(delays)
    return delays

def getGroupCoeff(delays,Fs,fc,N):
    coeff = np.zeros((N,256))
    for i in range(N):
        coeff[i,:] = calcFilterCoeff(delays[i],Fs,fc)
    return coeff
    
def plotFilterTaps(coeff,N):
    Taps=np.arange(0,len(coeff),1)
    plt.figure()
    plt.stem(Taps,coeff,use_line_collection=True)
    plt.title("Filter Taps")
    plt.xlabel("Tap #")
    plt.ylabel("Magnitude")
    
def freqResp(coeff,Fs):
    f, w = signal.freqz(coeff,1,fs=Fs)
    plt.figure()
    plt.plot(f,20*np.log10(abs(w)),'b')
    plt.ylabel('Amplitude [dB]')
    plt.xlabel('Frequency [rad/sample]')
    plt.title('Amplitude vs Frequency')
    plt.figure()
    plt.plot(f,np.unwrap(np.angle(w)),'g')
    plt.ylabel('Phase [radians]')
    plt.xlabel('Frequency [rad/sample]')
    plt.title('Phase vs Frequency')

def timeResp(coeff,Fs):
    t = np.arange(0,10e-3,1/Fs)
    wave = 10*np.sin(4e3*2*np.pi*t)
    plt.figure()
    plt.plot(t,wave)
    z=signal.lfilter(coeff,1,wave);
    plt.figure()
    plt.plot(t,z)
    
def writeVerilogFile(coeff,N):
    floatCoeff = ((2**(bits-1)-1)*Coeff)
    intCoeff = floatCoeff.astype(np.int16)
    coeff = intCoeff
    for j in range(N):
        a_file = open("verilogcoeff"+str(j)+".txt","w")
        for i in range(256):
            a_file.write("coeff["+str(i)+"] = 12'd"+str(coeff[j,i])+";\n")
        a_file.close()
        
def writeCoeffFile(coeff,N):
    floatCoeff = ((2**(bits-1)-1)*Coeff)
    intCoeff = floatCoeff.astype(np.int16)
    a_file = open("coeff.txt","w")
    for row in intCoeff:
        np.savetxt(a_file,row)
    a_file.close()
    
steerAngle = 45; # degrees
Fs = 44.1e3 # Hz
v = 343 # meters/s
dx = .3 # meters
fc = 22e3
N = 4 # number of Microphones
bits = 12
a = getGroupDelays(N,steerAngle,v,dx)
Coeff = getGroupCoeff(a,Fs,fc,N)
#plotFilterTaps(Coeff[1,:],Fs)
timeResp(Coeff[2,:],Fs)
writeVerilogFile(Coeff,4)
