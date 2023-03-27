import math

# (1) Convert to gaussian
def Gm(x, Lm):
	return 1/(10*math.sqrt(2*math.pi)) * math.exp(-(x-Lm)**2/(2*100))
