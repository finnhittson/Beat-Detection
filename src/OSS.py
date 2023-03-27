from scipy.io import wavfile
import scipy
import numpy as np
import math
import plotters

# (1) Overlap
def overlap(filepath, framesize:int=1024, hop:int=128):
	sr, data = read_wav(filepath)
	#plotters.plot_signal(data, sr)
	frames = get_frames(data, framesize, hop)
	#plotters.plot_frames(f, title="Frame")
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
    return [[math.log(abs(comp)) for comp in frame] for frame in fft_frames]


# (3) Flux
def get_flux(log_power, fft_frames):
	flux = []
	for n in range(1,len(log_power)):
		flux.append(0)
		N = 0
		for k in range(1,512):#range(1, len(log_power[n])):
			if abs(fft_frames[n,k]) > abs(fft_frames[n-1,k]):
				N += 1
				flux[-1] += log_power[n,k] - log_power[n-1,k]
		#print(f"number of fft bins representing positive frequencies: {N}")
	return flux


# (4) Low-pass Filter
def low_pass_filter(flux):
	b = scipy.signal.firwin(numtaps=14, cutoff=7, fs=344.5)
	y = []
	for n in range(len(flux)):
		y.append(0)
		for i in range(14):
			if n > i:
				y[-1] += b[i]*flux[n-i]
	return y

