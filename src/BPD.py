import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import math
import OSS as oss

# (1) Overlap
def overlap(data, framesize:int=2048, hop:int=128):
	#oss.plot_signal(data)
	#oss.plot_frames(frames, hop=hop)
	return oss.get_frames(data, framesize, hop)

# (2) Generalized autocorrelation 
def generalized_autocorrelation(frames, c:float=0.5):
	dft = np.fft.fft(frames)
	return 	np.fft.ifft(pow(abs(dft), c))

# (3) Enhance harmonics
def enhance_harmonics(A):
	for t in range(len(A)):
		if 2*t < len(A):
			A[t] += A[2*t]
		if 4*t < len(A):
			A[t] += A[4*t]
	return A

# (4) Pick peaks
def pick_peaks(A, framesize:int=2048, hop:int=128):
	y = [np.array(A[0])]
	for frame in A[1:]:
		y = np.concatenate((y, A[-hop:]), axis=None)
	A = y[98:414]
	peaks = []
	last = 0
	for i in range(1, len(A)-1):
		if A[i] >= A[i-1] and A[i] >= A[i+1] and i-1 != last:
			last = i
			peaks.append((i, A[i]))
	peaks.sort(key=lambda a: a[1])
	peaks = list(map(list, zip(*peaks)))
	indices = peaks[0]
	values = peaks[1]
	return indices[-10:], values[-10:]

# Plotting functions
def plot_correlation(A, indices:list=None, values:list=None, title:str="set me"):
	plt.figure().set_figheight(2)
	plt.plot(abs(A[0][98:414]))
	if indices is not None and values is not None:
		for i in range(len(indices)):
			plt.scatter(indices[i], abs(values[i]), c='k', s=15, marker='s', zorder=10)

	ticks = np.arange(2, 303, 100)
	labels = np.arange(100, 401, 100)
	plt.xticks(ticks=ticks, labels=labels)
	plt.xlabel("lag (samples)")
	plt.ylabel("mag.")
	plt.title(title)
	plt.show()
