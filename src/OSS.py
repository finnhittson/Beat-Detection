import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import math

# (1) Overlap
def overlap(filepath, framesize:int=1024, hop:int=128):
	sr, data = read_wav(filepath)
	#plot_signal(data, sr)
	f = frames(data, framesize, hop)
	#plot_frames(f, title="Frame")
	return f

def read_wav(filepath):
	sr, data = wavfile.read(filepath)
	return sr, data

def frames(data, framesize, hop):
	frames = []
	tmp = []
	# add two audio stream check
	for i in range(len(data)):
		tmp.append(data[i])
		if len(tmp) == framesize:
			frames.append(tmp)
			tmp = tmp[-hop:]
	return np.array(frames)

# (2) Log Power Spectrum
def low_power_spectrum(frames):
	tappered_frames = hamming_window(frames)
	fft_frames = np.fft.fft(tappered_frames)
	lp = np.array(log_power(fft_frames))
	plot_frames(lp, title="Log Power Spectrum", scatter=True)
	return lp, fft_frames

def hamming_window(frames):
	M = len(frames[0])
	t = np.linspace(-M/2, M/2, M)
	window = np.array([0.54 - 0.46*math.cos(2*math.pi*i/(M-1)) for i in t])
	return np.array([frame*window for frame in frames])

def log_power(fft_frames):
	log_power = []
	for frame in fft_frames:
		tmp = []
		for amp in frame:
			tmp.append(math.log(1 + 1000*abs(amp)))
		log_power.append(tmp)
	return np.array(log_power)


# (3) Flux
def flux(lp, fft_frames):
	flux = []
	for n in range(1,len(lp)):
		frame_flux = 0
		for k in range(len(lp[n])):
			if abs(fft_frames[n,k]) - abs(fft_frames[n-1,k]) > 0:
				frame_flux += lp[n,k] - lp[n-1,k]
		flux.append(frame_flux)
	#plot_flux(flux)
	return flux


# (4) Low-pass Filter


# Plotting functions
def plot_signal(data, sr:int=44100, endtime:int=6):
	# FIX: add two audio stream check
	y = data[:endtime*sr]
	x = list(range(len(y)))
	plt.plot(x, y, 'k', linewidth=0.2)
	plt.show()

def plot_frames(frames, sr:int=44100, endtime:int=6, hop:int=128, title:str="Frames", scatter:str=False):
	y = np.array([])
	for idx, frame in enumerate(frames):
		if idx == 0: y = frame
		else: y = np.concatenate((y, frame[128:]), axis=None)
	y = y[:endtime*sr]
	x = list(range(len(y)))
	
	if scatter:
		plt.scatter(x, y, c='k', s=0.1)
	else:
		plt.plot(x, y, 'k', linewidth=0.1)
	
	plt.xlabel("time/seconds", fontsize=16)
	if title == "Frames":
		plt.ylabel("audio", fontsize=16)
	else:
		plt.ylabel("freq/kHz", fontsize=16)
		plt.ylim([0,20])
		plt.yticks([0,5,10,15,20])
	plt.title(title, fontsize=18)
	
	plt.show()

def plot_flux(flux, sr:int=44100, endtime:int=6):
	y = flux[:endtime*sr]
	x = list(range(len(y)))
	plt.plot(x, flux, 'k', linewidth=0.5)
	plt.xlabel("time/seconds", fontsize=16)
	plt.ylabel("flux", fontsize=16)
	plt.title("Flux", fontsize=18)
	plt.show()
