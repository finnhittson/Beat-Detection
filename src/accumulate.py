import math

# (1) Convert to gaussian
def Gm(x, Lm):
	return 1/(10*math.sqrt(2*math.pi)) * math.exp(-(x-Lm)**2/(2*100))

# (2) Accumulator
def accumulate(Lms):
	y = []
	for x in range(414):
		y.append(0)
		for Lm in Lms:
			y[-1] += (Gm(x, Lm))
	return y