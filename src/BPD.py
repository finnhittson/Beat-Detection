import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import math
import OSS as oss

# (1) Overlap
def overlap(data, framesize:int=2048, hop:int=128):
	#oss.plot_signal(data)
	#oss.plot_frames(frames, hop=hop)
	return oss.frames(data, framesize, hop)
