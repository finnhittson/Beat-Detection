import matplotlib.pyplot as plt
import numpy as np

#x = [0,1,2,3]
#y = [1,1,1,1]
#x = [0, 1.5, 3, 4.5]
#y = [0.5, 0.5, 0.5, 0.5]
#x = [0,2,4,6]
#y = [0.5, 0.5, 0.5, 0.5]

x = [0, 1, 1.5, 2, 3.5, 4, 4.5, 6]
y = [2, 1, 0.5, 1.5, 1.5, 0.5, 0.5, 0.5]

plt.figure().set_figheight(2)
markerline, stemlines, baseline = plt.stem(x,y, basefmt=" ")
plt.setp(stemlines, 'linewidth', 3)
plt.setp(markerline, markersize = 10)
plt.ylim([0,2.3])
plt.xlim([-0.5,6.5])
plt.xticks(ticks=[0,2,4,6], labels=["0P", "2P", "4P", "6P"], fontsize=15)
plt.yticks(ticks=[0,1,2], labels=[0,1,2], fontsize=15)
plt.ylabel("amplitude", fontsize=16)
plt.title("Combined $I_{P,\\phi}$", fontsize=20)
plt.show()