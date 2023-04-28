import OSS as oss
import BPD as bpd
import accumulate as acc
import argparse
import scipy
import numpy as np

def run_beat_detection(filepath, framesize, hop):
	# (1) OSS
	frames = oss.overlap(filepath=filepath, framesize=framesize, hop=hop)
	log_power, fft_frames = oss.low_power_spectrum(frames)
	flux = oss.comp_flux(log_power=log_power)
	filtered_signal = oss.low_pass_filter(flux)

	# (2) BPD
	oss_frames = bpd.overlap(data=flux, framesize=2048, hop=hop)
	Am = bpd.generalized_autocorrelation(frames=oss_frames, c=0.5)
	#EAC = enhance_harmonics(A=Am)
	indices, values = bpd.pick_peaks(A=Am)
	Lm = bpd.evaluate_pulse_train(peaks=indices[0], frame=oss_frames[0])

	# (3) Accumulation
	Lms = acc.eval_entire_signal(indices, values)
	y = acc.accumulate_gauss(Lms=Lms)
	idxs, vals = bpd.find_local_maximums(np.concatenate((np.zeros(98), y[98:])))

	return 344.5*60/idxs[-1]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run beat detection algorithm on a song")
	parser.add_argument(
		"--path",
		metavar="path",
		type=str,
		help="Path to song file.")
	parser.add_argument(
		"--framesize",
		metavar="framesize",
		type=int,
		help="Size of framse to spilt data on.")
	parser.add_argument(
		"--hop",
		metavar="hop",
		type=int,
		help="Hop size when splitting data.")

	parser.set_defaults(framesize=1024, hop=128)
	args = parser.parse_args()
	beat_estimate = run_beat_detection(args.path, args.framesize, args.hop)
	print(beat_estimate)