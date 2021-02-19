from matplotlib import pyplot as plt 
import scipy as sp 
from scipy import signal as spsig
import numpy as np     


def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    t = np.arange(0,length_secs,1/sampling_rate_Hz)
    x = amplitude * np.sin(2*np.pi*frequency_Hz*t + phase_radians)
    return (t, x)

def main():
    fs=44100
    (t,x) = generateSinusoidal(1.0, fs, 400, 0.5, np.pi/2)
    # (t_sq,x_sq) = generateSquare(1.0, fs, 400, 0.5, 0)

    # plt.plot(t,x)   # need to limit to first 5 ms
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')
    # plt.title('generateSinusoidal() output')
    # plt.xlim([0, 0.005])
    # plt.show()

    Xdft = np.fft.fft(x)
    XRe = np.real(Xdft)
    XIm = np.imag(Xdft)
    XAbs = np.abs(Xdft)
    XPhase = np.angle(Xdft)
    XPhase[np.abs(Xdft) < 1] = 0

    f1 = np.fft.fftfreq(len(Xdft), d=1/fs)
    f2 = np.empty(len(Xdft))
    for i in range(len(Xdft)):
        f2[i] = i * (fs/len(Xdft))


    print(len(Xdft))
    print(f1.all()==f2.all())
    # print(f2)


    # plt.subplot(1,2,1)
    # plt.plot(f,XPhase)             # Phase response
    # plt.xlim(left=0,right=r_bound)
    # plt.title('400 Hz '+ label +' Phase Response')
    # plt.ylabel('Phase (radians)')
    # plt.xlabel('Frequency (radians)')

    # plt.subplot(1,2,2)
    # plt.plot(f,XAbs)               # Magnitude response
    # plt.xlim(left=0,right=r_bound)
    # plt.title('400 Hz '+ label +' Magnitude Response')
    # plt.ylabel('Magnitude (energy)')
    # plt.xlabel('Frequency (Hz)')

    # plt.subplots_adjust(wspace=0.5)
    # plt.show()

main()