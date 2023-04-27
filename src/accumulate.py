import math
import BPD as bpd
import numpy as np

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

def eval_entire_signal_author(peaks, frames):
	bphase = np.zeros(414)
	for idx, frame in enumerate(frames):
		tempo_scores = np.zeros(len(peaks[idx])) 
		onset_scores = np.zeros(len(peaks[idx]))
		for j, bpm in enumerate(peaks[idx]):
			mag, var = calc_pulse_trains_authors(bpm=bpm, window=frame, sr=44100)
			tempo_scores[j] = mag
			onset_scores[j] = var

		tempo_scores /= sum(tempo_scores)
		onset_scores /= sum(onset_scores)

		combo_scores = tempo_scores + onset_scores
		combo_scores /= combo_scores.sum()

		# find best score
		besti = combo_scores.argmax()
		bestbpm = peaks[idx][besti]
		beststr = combo_scores[besti]


		bphase[ int(bestbpm) ] += beststr
	bpm = bphase.argmax()
	return bpm, bphase

def calc_pulse_trains_authors(bpm, window, sr):
    num_offsets = int(round(60.0 * sr / bpm))
    period = num_offsets
    samples = len(window)

    bp_mags = np.zeros(num_offsets)
    for phase in range(samples-1, samples-1-period, -1):
        mag = 0.0
        for b in range(4):
            ind = int(phase - b*period)
            if ind >= 0:
                mag += window[ind]

            # slow down by 2
            ind = int(phase - b*period*2)
            if ind >= 0:
                mag += 0.5*window[ind]

            # slow down by 3
            ind = int(phase - b*period*3/2)
            if ind >= 0:
                mag += 0.5*window[ind]
        bp_mags[samples-1-phase] = mag

    bp_max = max(bp_mags)
    bp_var = np.var(bp_mags)
    return bp_max, bp_var
