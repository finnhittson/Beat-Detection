from scipy.io import wavfile
import scipy
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
	dft = np.fft.fft(a=frames)
	return 	np.fft.ifft(pow(abs(dft), c)).real

def autocorrelation(signal, c:float=0.5):
    N = signal.shape[1]
    ffts = scipy.fftpack.fft(signal, 2*N, axis=1) / (2*N)
    ffts_abs = abs(ffts)
    ffts_abs_scaled = ffts_abs**c
    scratch = (scipy.fftpack.ifft(ffts_abs_scaled, axis=1).real)*(2*N)
    xcorr = scratch[:,:N]
    return xcorr

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
	y = flatten_signal(A)
	indices = []
	values = []
	for i in range(98, len(y), 316):
		idxs, vals = find_local_maximums(y[i:i+316])
		indices.append(idxs)
		values.append(vals)
	return indices, values

def find_local_maximums(A):
	peaks = []
	last = 0
	for i in range(1, len(A)-1):
		if A[i-1] <= A[i] >= A[i+1] and i-1 != last:
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
	for peak in peaks:
		amp, indices = create_pulse_train(peak)
		ccs.append(moving_dot_product(peak, frame, amp, indices))

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
		SCv.append(np.var(cc))
		SCx.append(max(cc))
	SCv = np.array(SCv)
	SCx = np.array(SCx)
	return SCv/np.linalg.norm(SCv), SCx/np.linalg.norm(SCx)

def moving_dot_product(peak, frame, amp, indices):
	cc_values = np.zeros(peak)
	for phase in range(peak):
		if indices[-1]+phase < len(frame):
			for idx, index in enumerate(indices):
				cc_values[phase] += frame[index+phase]*amp[idx]
	return cc_values

def create_pulse_train(P):
	indices = np.array([0, 1, 1.5, 2, 3, 4, 4.5, 6])*P
	amp = np.array([2, 1, 0.5, 1.5, 1.5, 0.5, 0.5, 0.5])
	return amp, indices.astype(np.int32)

def flatten_signal(frames, hop:int=128):
	y = frames[0]
	for frame in frames[1:]:
		y = np.concatenate((y, frame[-128:]))
	return y