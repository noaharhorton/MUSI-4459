from matplotlib import pyplot as plt 
import scipy as sp 
from scipy import signal as spsig
import numpy as np 

def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    t = np.arange(0,length_secs,1/sampling_rate_Hz)
    x = amplitude * np.sin(2*np.pi*frequency_Hz*t + phase_radians)
    return (t, x)

def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    (t, x) = generateSinusoidal(0, sampling_rate_Hz, 0, length_secs, phase_radians)
    numHarm = 10
    dummy_t = 0
    for i in range(numHarm):
        if i%2==0:
            x += generateSinusoidal(amplitude/(i+1), sampling_rate_Hz, frequency_Hz*(i+1), length_secs, phase_radians)[1]
    return (t,x)

def computeSpectrum(x, sample_rate_Hz, window_type):
    if window_type == 'rect':
        env_x = spsig.get_window('boxcar', len(x)) * x
    if window_type == 'hann':
        env_x = spsig.get_window('hann', len(x)) * x
    Xdft = np.fft.fft(env_x)
    XRe = np.real(Xdft)
    XIm = np.imag(Xdft)
    XAbs = np.abs(Xdft)
    XPhase = np.angle(Xdft)
    XPhase[np.abs(Xdft) < 1] = 0    # only looks at phase at frequencies with non-zero magnitude; gets rid of noise/makes plots easier to read
                                    # Prof Beck said noise is expected in phase plots so comment out above line for the expected noise

    f = np.empty(len(Xdft))
    for i in range(len(Xdft)):
        f[i] = i * (sample_rate_Hz/len(Xdft))
    
    return(f, XAbs, XPhase, XRe, XIm)

def sineSweep(f1, f2, dur, fs):
    t = np.linspace(0, dur, dur*fs)
    x = np.sin(2*np.pi*(f1*t + (t**2)*(f2-f1)/2*dur))
    return(t, x)

def main():
    fs = 44100
    
    # Part 1 ------------------------------------
    (t_sin,x_sin) = generateSinusoidal(1.0, fs, 400, 0.5, np.pi/2)
    # plt.plot(t_sin,x_sin)   # need to limit to first 5 ms
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')
    # plt.title('generateSinusoidal() output')
    # plt.xlim([0, 0.005])
    # plt.show()

    # Part 2 ------------------------------------
    (t_sq,x_sq) = generateSquare(1.0, fs, 400, 0.5, 0)
    # plt.plot(t_sq,x_sq)
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')
    # plt.title('generateSquare() output')
    # plt.xlim([0, 0.005])
    # plt.show()

    # Parts 3, 4 ------------------------------------
    window_type = 'rect'        # just change these two lines for hann/rect window
    x = x_sq                    # or for x_sin/x_sq

    if x.all() == x_sin.all():      # makes changing between waveshapes easier
        r_bound = 1000
        label = 'Sine'
    elif x.all() == x_sq.all():
        r_bound = 5000
        label = 'Square'
    
    (f, XAbs, XPhase, XRe, XIm) = computeSpectrum(x, fs, window_type)

    plt.subplot(1,2,1)
    plt.plot(f,XPhase)             # Phase response
    plt.xlim(left=0,right=r_bound)
    plt.title('400 Hz '+ label +' Phase Response')
    plt.ylabel('Phase (radians)')
    plt.xlabel('Frequency (radians)')

    plt.subplot(1,2,2)
    plt.plot(f,XAbs)               # Magnitude response
    plt.xlim(left=0,right=r_bound)
    plt.title('400 Hz '+ label +' Magnitude Response')
    plt.ylabel('Magnitude (energy)')
    plt.xlabel('Frequency (Hz)')

    plt.subplots_adjust(wspace=0.5)
    plt.show()

    # Part 5 ------------------------------------
    # (t,x) = sineSweep(1,20,5,fs)
    # # plt.plot(t,x)
    # # plt.show()
    # (f, XAbs, XPhase, XRe, XIm) = computeSpectrum(x, fs, 'rect')

    # plt.subplot(1,2,1)
    # plt.plot(f,XPhase)             # Phase response
    # plt.xlim(left=-2000,right=2000)
    # plt.title('Sine Sweep Phase Response')
    # plt.ylabel('Phase (radians)')
    # plt.xlabel('Frequency (radians)')

    # plt.subplot(1,2,2)
    # plt.plot(f,XAbs)               # Magnitude response
    # plt.xlim(left=-2000,right=2000)
    # plt.title('Sine Sweep Magnitude Response')
    # plt.ylabel('Magnitude (energy)')
    # plt.xlabel('Frequency (Hz)')

    # plt.subplots_adjust(wspace=0.5)
    # plt.show()

main()