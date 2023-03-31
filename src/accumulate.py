import math
import BPD as bpd

# (1) Convert to gaussian
def Gm(x, Lm):
	return 1/(10*math.sqrt(2*math.pi)) * math.exp(-(x-Lm)**2/(2*100))

# (2) Accumulator
def accumulate_gauss(Lms):
	y = []
	for x in range(414):
		y.append(0)
		for Lm in Lms:
			y[-1] += (Gm(x, Lm))
	return y

def eval_entire_signal(peaks, frames):
	signal = bpd.flatten_signal(frames)
	Lms = []
	for idx, peak_set in enumerate(peaks):
		Lms.append(bpd.evaluate_pulse_train(peak_set, signal[98+316*idx:414+316*idx]))
	return Lms
