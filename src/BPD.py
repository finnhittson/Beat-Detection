from scipy.io import wavfile
import numpy as np
import math
import OSS as oss

# (1) Overlap
def overlap(data, framesize:int=2048, hop:int=128):
	#plotters.plot_signal(data)
	#plotters.plot_frames(frames, hop=hop)
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
def pick_peaks(A, hop:int=128):
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

# (5) Evaluate pulse trains
def evaluate_pulse_train(peaks, frame):
	ccs = []
	for P in peaks:
		amp, indices = create_pulse_train(P)
		ccs.append(moving_dot_product(P, frame, amp, indices))

	SCv, SCx = max_var_score(ccs)
	SCv_sum = sum(SCv)
	SCx_sum = sum(SCx)
	SC = [SCv[i]/SCv_sum + SCx[i]/SCx_sum for i in range(len(SCv))]
	tempo_idx = max(list(range(len(SC))), key=SC.__getitem__)
	return peaks[tempo_idx]

def max_var_score(ccs):
	SCv = []
	SCx = []
	for cc in ccs:
		SCv.append(variance(cc))
		SCx.append(max(cc))
	SCv = np.array(SCv)
	SCx = np.array(SCx)
	return SCv/np.linalg.norm(SCv), SCx/np.linalg.norm(SCx)

def variance(x):
	n = len(x)
	x_bar = sum(x)/n
	return math.sqrt(sum([(x[i]-x_bar)**2 for i in range(n)])/(n-1))

def moving_dot_product(P, frame, amp, indices):
	cc_values = []
	for phase in range(P):
		cc_values.append(0)
		if indices[-1]+phase < len(frame):
			for idx, index in enumerate(indices):
				cc_values[-1] += frame[index+phase]*amp[idx]
	return cc_values

def create_pulse_train(P):
	indices = [int(i*P) for i in [0, 1, 1.5, 2, 3, 4, 4.5, 6]]
	amp = [2, 1, 0.5, 1.5, 1.5, 0.5, 0.5, 0.5]
	return amp, indices
