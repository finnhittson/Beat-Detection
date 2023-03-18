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
def pick_peaks(A):
	peaks = []
	last = 0
	for i in range(1, len(A)-1):
		if A[i] >= A[i-1] and A[i] >= A[i+1] and i-1 != last:
			last = i
			peaks.append((i, A[i]))
	peaks.sort(key=lambda a: a[1])
	return list(map(list, zip(*peaks)))[-10:]

