import numpy as np 
import scipy as sp
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

def crossCorr(x,y):
    x = x/x.std()
    y = y/y.std()
    # n = len(x)
    return signal.correlate(x,y,mode='same')
    # / np.sqrt(signal.correlate(x,x,mode='same')[int(n/2)] * signal.correlate(y,y,mode='same')[int(n/2)])

def loadSoundFile(filename):
    rate, data = wavfile.read(filename)
    leftCh = data[:,0]
    return leftCh

def findSnarePosition(snareFilename, drumloopFileName):
    snare = loadSoundFile(snareFilename)
    drums = loadSoundFile(drumloopFileName)
    corr = crossCorr(snare, drums)
    snarePos = signal.find_peaks(corr,height=980, distance=6000)
    print(len(snarePos[0]))
    return snarePos

def main():
    snare = loadSoundFile('c:\\Users\\noaha\Desktop\MUSI 4459\Assignment 1\snare.wav')
    drums = loadSoundFile('c:\\Users\\noaha\Desktop\MUSI 4459\Assignment 1\drum_loop.wav')

    z = crossCorr(snare, drums)
    if len(snare) > len(drums):
        t = np.arange(0,len(snare))
    else:
        t = np.arange(0,len(drums))

    # plt.title('Correlation Graph')
    # plt.xlabel('Time')
    # plt.ylabel('Correlation')
    # plt.plot(z)
    # plt.savefig('01-correlation.png')
    # plt.show()
    a = findSnarePosition('c:\\Users\\noaha\Desktop\MUSI 4459\Assignment 1\snare.wav','c:\\Users\\noaha\Desktop\MUSI 4459\Assignment 1\drum_loop.wav')
    np.savetxt('./02-snareLocation.txt',a[0])



main()