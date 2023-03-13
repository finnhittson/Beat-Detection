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

# (2) Generalized Autocorrelation 
def generalized_autocorrelation(frames, c:float=0.5):
	dft = np.fft.fft(frames)
	return 	np.fft.ifft(pow(abs(dft), c))

# (3) Enhance Harmonics
def enhance_harmonics(A):
	for t in range(len(A)):
		if 2*t < len(A):
			A[t] += A[2*t]
		if 4*t < len(A):
			A[t] += A[4*t]
	return A

