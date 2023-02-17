import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import math
import OSS as oss

# (1) Overlap
def overlap(data, framesize:int=2048, hop:int=128):
	#oss.plot_signal(data)
	#oss.plot_frames(frames, hop=hop)
	return frames(data, framesize, hop)

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