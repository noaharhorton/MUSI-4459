import numpy as np 
from scipy import signal as sp
from scipy.io import wavfile as spwav
from matplotlib import pyplot as plt
from time import time as time
import os

# if len(x)=200 and len(h)=100, then the length of their convolution will be 200+100-1=299
def myTimeConv(x,h):
    convLen = len(x) + len(h) - 1
    y = np.zeros(convLen, dtype=np.float64)

    for i in range(convLen):

        for k in range(len(h)):
            if k+i<len(x):
                y[i] += h[k] * x[k+i]
            else:
                y[i] += h[k] * 0

    return y

def CompareConv(x,h):
    convLen = len(x) + len(h) - 1
    t1 = time()
    my_y = myTimeConv(x,h)
    t2 = time()
    sp_y = sp.convolve(x,h)
    t3 = time()
  
    m = np.mean(sp_y) - np.mean(my_y)
    mabs = abs(m)
    stdev = np.std(sp_y) - np.std(my_y)
    t = [t2-t1, t3-t2]

    return(m, mabs, stdev, t)

def main():
    # x = np.ones(200)
    # h = np.concatenate((np.arange(0,1,1/25), np.linspace(1,0,num=26)))

    # y_time = myTimeConv(x,h)
    # plt.plot(y_time)
    # plt.xlabel('Samples')
    # plt.ylabel('Amplitude')
    # plt.title('Convolution of x*h')
    # plt.show()

    [_, x] = spwav.read('./audio/piano.wav')
    [_, h] = spwav.read('./audio/impulse-response.wav')
    [m, mabs, stdev, t] = CompareConv(x,h)
    # When I run this with the files as inputs, I keep getting 
    # RuntimeWarning: overflow encountered in short_scalars
    # and I can't find out how to fix it


main()