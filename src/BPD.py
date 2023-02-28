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
def get_gen_autoc(oss_frames, c:float=0.5):
	dft = np.fft.fft(oss_frames)
	return 	np.fft.ifft(pow(abs(dft), c))

# (3) Enhance Harmonics
