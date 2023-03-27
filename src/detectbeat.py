import OSS as oss
import BPD as bpd
import argparse
import scipy

def run_beat_detection(filepath, framesize, hop):
	# (1) OSS
	frames = oss.overlap(filepath=filepath, framesize=framesize, hop=hop)
	log_power, fft_frames = oss.low_power_spectrum(frames)
	flux = oss.get_flux(log_power, fft_frames)
	filtered_signal = oss.low_pass_filter(flux, n=len(flux))

	# (2) BPD
	oss_frames = bpd.overlap(data=flux, framesize=2048, hop=hop)
	Am = bpd.generalized_autocorrelation(oss_frames=oss_frames, c=0.5)
	enhanced_signal = enhance_harmonics(A=Am)
	indices, values = bpd.pick_peaks(A=EAC, hop=128)
	Lm = bpd.evaluate_pulse_train(indices, oss_frames[0])


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
	run_beat_detection(args.path, args.framesize, args.hop)