import OSS as oss
import BPD as bpd
import argparse

def run_beat_detection(filepath, framesize, hop):
	# OSS
	frames = oss.overlap(filepath=filepath, framesize=framesize, hop=hop)
	log_power, fft_frames = oss.low_power_spectrum(frames)
	#flux = oss.flux(log_power, fft_frames)

	# BPD
	#frames = bpd.overlap(data=flux, framesize=2048, hop=hop)

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

	parser.set_defaults(path="song.wav", framesize=1024, hop=128)
	args = parser.parse_args()
	run_beat_detection(args.path, args.framesize, args.hop)