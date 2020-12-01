# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 19:33:25 2020

@author: drewd
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



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
def getFractionalDelay(delays,Fs,N):
    sampleDelay = delays*Fs
    buffer = np.zeros(N)
    fracDelay = np.zeros(N)
    for i in range(len(delays)):
         buffer[i] = np.floor(sampleDelay[i])
         fracDelay[i] = sampleDelay[i] - buffer[i]
    return buffer, fracDelay
def getFIRCoeff(fracDelay,filterLen,N):
    coeff = np.zeros([N,filterLen])
    for i in range(N):
        centerTap = round(filterLen/2)
        for j in range(filterLen):
            x = j-fracDelay[i];
            sinc = np.sin(np.pi*(x-centerTap))/(np.pi*(x-centerTap))
            window = .54-.46*np.cos(2*np.pi*(x+.5)/filterLen)
            coeff[i][j] = window*sinc
            if x-centerTap == 0:
                coeff[i][j] = 1
            if abs(coeff[i][j])<.000000003:
                coeff[i][j] = 0
        
    return coeff
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
def h(k,coeff):
    return coeff[k]
def x(n,k,wave):
    if n-k < 0:
        return 0
    else:
        a = n-k
        return wave[a]
def FilterOverallResponse(wave,buffer,coeff):
    outputLength = int(buffer+len(wave))
    output = np.zeros(outputLength)
    for i in range(len(wave)):
        for k in range(len(coeff)):
            output[i+int(buffer)] = output[i+int(buffer)]+h(k,coeff)*x(i,k,wave)
    return output
steerAngle = 60; # degrees
Fs = 44.1e3 # Hz
v = 343 # meters/s
dx = .3 # meters
fc = 22e3
N = 8 # number of Microphones
bits = 12

delays = getGroupDelays(N,steerAngle,v,dx)
buffer,FracDelay = getFractionalDelay(delays,Fs,N)
coeff = getFIRCoeff(FracDelay,31,N)
coeff = (2**(12-1)-1)*coeff
coeff = coeff.astype(np.int32)
plt.figure()
plt.plot(coeff[0,:])
n = np.arange(0,10e-3,1/Fs)
wave = np.sin(2*np.pi*150*n)
wave = (2**(12-1)-1)*wave
wave = wave.astype(np.int32)
plt.figure()
plt.plot(wave)
y = FilterOverallResponse(wave,buffer[0],coeff[0,:])
plt.plot((y/max(y)*max(wave)))