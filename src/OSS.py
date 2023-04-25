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
    return [[math.log(1+1000*abs(comp)) for comp in frame] for frame in fft_frames]


# (3) Flux
def comp_flux_author(log_power):
	flux = np.zeros(log_power.shape[0])
	prev = np.zeros(log_power.shape[1])
	for i in range(log_power.shape[0]):
		diff = log_power[i] - prev
		diff_reduced = diff[1:]
		diff_clipped = diff_reduced.clip(min=0)
		prev = np.copy(log_power[i])
		flux[i] = sum(diff_clipped)
	return flux

def comp_flux(log_power):
	flux = np.zeros(len(log_power))
	for n in range(1, len(log_power)):
		for k in range(len(log_power[n])):
			if abs(log_power[n,k]) > abs(log_power[n-1,k]):
				add = log_power[n,k] - log_power[n-1,k]
				flux[n] += add
	return flux


# (4) Low-pass Filter
def low_pass_filter(flux):
	b = scipy.signal.firwin(numtaps=15, cutoff=7, fs=344.5)
	y = np.zeros(len(flux)+1)
	for n in range(len(flux)):
		for i in range(15):
			if n > i:
				y[n] += b[i]*flux[n-i]
	return y

def low_pass_filter_author(flux):
	b = scipy.signal.firwin(numtaps=15, cutoff=6/44100/128/2)
	return scipy.signal.lfilter(b, 1.0, flux)