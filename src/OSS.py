import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy
import numpy as np
import math

# (1) Overlap
def overlap(filepath, framesize:int=1024, hop:int=128):
	sr, data = read_wav(filepath)
	#plot_signal(data, sr)
	frames = get_frames(data, framesize, hop)
	#plot_frames(f, title="Frame")
	return frames

# open and read .wav file
def read_wav(filepath):
    sr, data = wavfile.read(filepath)
    return sr, data

# parse audio signal into overlapping frames
def get_frames(data, framesize, hop):
    frames = []
    tmp = []
    for i in range(len(data)):
        tmp.append(data[i])
        if len(tmp) == framesize:
            frames.append(tmp)
            tmp = tmp[hop:]
    return np.array(frames)


# (2) Log Power Spectrum
def low_power_spectrum(frames):
	tappered_frames = hamming_window(frames)
	fft_frames = np.fft.fft(tappered_frames)
	log_power = np.array(comp_log_power(fft_frames))
	return log_power, fft_frames

# multiplies frames by the hamming window function
def hamming_window(frames):
    window = scipy.signal.hamming(M=len(frames[0]))
    return np.array([frame*window for frame in frames])

# computes the log power spectrum of the frequency bins
def comp_log_power(fft_frames):
    return [[math.log(1 + 1000*abs(comp)) for comp in frame] for frame in fft_frames]


# (3) Flux
def get_flux(log_power, fft_frames):
	flux = []
	for n in range(2,len(log_power)):
		frame_flux = 0
		for k in range(len(log_power[n])):
			if abs(fft_frames[n,k]) - abs(fft_frames[n-1,k]) > 0:
				frame_flux += log_power[n,k] - log_power[n-1,k]
		flux.append(frame_flux)
	return flux


# (4) Low-pass Filter
def low_pass_filter(flux, n):
    b = scipy.signal.firwin(numtaps=14, cutoff=7, fs=344.5)
    y = []
    for i in range(0, 14*math.floor(len(flux)/len(b)), 1):
        y.append(0)
        for j in range(14):
            if i > j:
                y[-1] += b[j]*flux[i-j]
    return y


# Plotting functions
def plot_signal(data, sr:int=44100, stop:int=6, title:str="Raw Signal"):
    y = data[:int(stop*sr)]
    x = list(range(len(y)))
    plt.figure().set_figheight(2)
    plt.plot(x, y, 'k', linewidth=0.2)
    plt.xlabel("time/seconds", fontsize=10)
    plt.ylabel("audio", fontsize=10)
    plt.title(title, fontsize=12)
    labels = list(range(0,7,1))
    ticks = [int(len(y)/stop)*i for i in labels]
    plt.xticks(ticks=ticks, labels=labels)
    labels = range(-1, 2, 1)
    ticks = [min(data), 0, max(data)]
    plt.yticks(ticks=ticks, labels=labels)
    plt.show()

def plot_frames(frames, sr:int=44100, stop:int=6, framesize:int=1024, hop:int=128, title:str="Overlap", scatter:str=False):
    y = np.array([frames[0]])
    for frame in frames[1:]:
            y = np.concatenate((y, frame[-128:]), axis=None)
    x = list(range(len(y)))
    plt.figure().set_figheight(2)
    if scatter:
        plt.scatter(x, y, c='k', s=0.1, marker='.')
    else:
        plt.plot(x, y, 'k', linewidth=0.2)

    plt.xlabel("time/seconds", fontsize=10)
    if title == "Overlap":
        plt.ylabel("audio", fontsize=10)
        labels = range(-1, 2, 1)
        ticks = [min(data), 0, max(data)]
        plt.yticks(ticks=ticks, labels=labels)
    else:
        plt.ylabel("freq/kHz", fontsize=10)
        #plt.yticks([0,5,10,15,20])
        
    labels = list(range(0,7,1))
    ticks = [sr*i for i in labels]
    plt.xticks(ticks=ticks, labels=labels)
    plt.title(title, fontsize=12)
    plt.show()

def plot_log_spectrum(fft_frames, framesize, hop, sr):
    fft_frames = abs(fft_frames)
    plt.figure().set_figheight(2)
    t = [[j+hop*i for j in range(framesize)] for i in range(len(fft_frames))]
    y = fft_frames.flatten()
    plt.scatter(t, y, c='k', s=0.1)

    plt.xlabel("time/seconds")
    plt.ylabel("freq/kHz")
    plt.title("Log Power Spectrum")
    #plt.yscale("log")

    labels = list(range(0,7,1))
    ticks = [sr*i for i in labels]
    plt.xticks(ticks=ticks, labels=labels)

    plt.show()

def plot_flux(y):
	plt.figure().set_figheight(2)

	x = list(range(len(y)))
	plt.plot(x, y, 'k', linewidth=0.5)
	
	plt.xlabel("time/seconds", fontsize=10)
	plt.ylabel("flux", fontsize=10)
	plt.title("Flux", fontsize=12)
	
	labels = list(range(0,7,1))
	ticks = [len(y)*i/6 for i in labels]
	plt.xticks(ticks=ticks, labels=labels)
	labels = [0, 20, 40, 60, 80]
	ticks = [max(y)*i/80 for i in labels]
	plt.yticks(ticks=ticks, labels=labels)
	
	plt.show()