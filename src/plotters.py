import matplotlib.pyplot as plt
import numpy as np

def plot_signal(data, sr:int=44100, stop:int=6, title:str="Raw Signal"):
    y = data[:int(stop*sr)]
    x = list(range(len(y)))
    plt.figure().set_figheight(2)
    plt.plot(x, y, 'k', linewidth=0.2)
    plt.xlabel("time/seconds", fontsize=10)
    plt.ylabel("audio", fontsize=10)
    plt.title(title, fontsize=12)
    labels = list(range(0,7,1))
    ticks = [int(len(y)/stop)*i for i in labels]
    plt.xticks(ticks=ticks, labels=labels)
    labels = range(-1, 2, 1)
    ticks = [min(data), 0, max(data)]
    plt.yticks(ticks=ticks, labels=labels)
    plt.show()

def plot_frames(frames, sr:int=44100, framesize:int=1024, hop:int=128, title:str="Overlap", scatter:str=False):
	if len(frames) > framesize:
		y = np.array([frames[0]])
		for frame in frames[1:]:
			y = np.concatenate((y, frame[-hop:]), axis=None)
	else: 
		y = frames

	x = list(range(len(y)))
	plt.figure().set_figheight(2)
	if scatter:
		plt.scatter(x, y, c='k', s=0.1, marker='.')
	else:
		plt.plot(x, y, 'k', linewidth=0.2)

	plt.xlabel("time/seconds", fontsize=10)
	if title == "Overlap":
		plt.ylabel("audio", fontsize=10)
		labels = range(-1, 2, 1)
		ticks = [min(abs(frames)), 0, max(abs(frames))]
		plt.yticks(ticks=ticks, labels=labels)
	else:
		plt.ylabel("freq/kHz", fontsize=10)
		#plt.yticks([0,5,10,15,20])

	labels = np.arange(0,len(y)/sr+1,1)
	ticks = [sr*i for i in labels]
	plt.xticks(ticks=ticks, labels=labels)
	plt.title(title, fontsize=12)
	plt.show()

def plot_log_spectrum(fft_frames, framesize, hop, sr):
    plt.figure().set_figheight(2)
    t = [[j+hop*i for j in range(framesize)] for i in range(len(fft_frames))]
    y = fft_frames.flatten()
    plt.scatter(list(range(len(y))), y, c='k', s=0.1)

    plt.xlabel("time/seconds")
    plt.ylabel("freq/kHz")
    plt.title("Log Power Spectrum")
    #plt.yscale("log")

    labels = list(range(0,7,1))
    ticks = [sr*i for i in labels]
    plt.xticks(ticks=ticks, labels=labels)

    plt.show()

def plot_flux(y, title:str="set me!"):
	plt.figure().set_figheight(2)

	x = list(range(len(y)))
	plt.plot(x, y, 'k', linewidth=0.5)
	
	plt.xlabel("time/seconds", fontsize=10)
	plt.ylabel("flux", fontsize=10)
	plt.title(title, fontsize=12)
	
	labels = list(range(0,7,1))
	ticks = [len(y)*i/6 for i in labels]
	plt.xticks(ticks=ticks, labels=labels)
	labels = [0, 20, 40, 60, 80]
	ticks = [max(y)*i/80 for i in labels]
	plt.yticks(ticks=ticks, labels=labels)
	
	plt.show()

def plot_correlation(A, start:int=98, stop:int=414, indices:list=None, values:list=None, title:str="set me"):
	plt.figure().set_figheight(2)
	plt.plot(abs(A[start:stop]))
	if indices is not None and values is not None:
		for i in range(len(indices)):
			plt.scatter(indices[i], abs(values[i]), c='k', s=15, marker='s', zorder=10)

	ticks = np.arange(2, 303, 100)
	labels = np.arange(100, 401, 100)
	plt.xticks(ticks=ticks, labels=labels)
	plt.xlabel("lag (samples)")
	plt.ylabel("mag.")
	plt.title(title)
	plt.show()

def plot_gaussian(Lm, g, title:str="set me"):
	plt.figure().set_figheight(2)
	if isinstance(Lm, int):
		y = [g(Lm, x) for x in range(414)]
		plt.plot(y)
	elif isinstance(Lm, list):
		plt.plot(Lm)
	else:
		print(f"type {type(Lm)} not supported")

	#plt.ylim([0,0.05])
	plt.title(title)
	plt.xlabel("lag (samples)")
	plt.ylabel("mag.")
	plt.show()