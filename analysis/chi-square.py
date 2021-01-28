import sys
import json
import numpy as np


# Command line arguments: input files
# First input is observed values with some subset
# Second argument is expected values of whole set
INPUT_FILE_1 = sys.argv[1]
INPUT_FILE_2 = sys.argv[2]


# Whole set
with open(INPUT_FILE_1) as f:
    A = json.load(f).values()
    A_size = sum(len(x) for x in A)

# Subset
with open(INPUT_FILE_2) as f:
    B = json.load(f).values()
    B_size = sum(len(x) for x in B)

# Divide the colorspace to n**3 cubes
n = 2

# Calculate chi-square for given subset
O = np.zeros(n**3)
E = np.zeros(n**3)

for colors in B:
    for color in colors:
        x = int(round(color[0]/255))
        y = int(round(color[1]/255))
        z = int(round(color[2]/255))
        O[n**2*x + n*y + z] += 1

for colors in A:
    for color in colors:
        x = int(round(color[0]/255))
        y = int(round(color[1]/255))
        z = int(round(color[2]/255))
        E[n**2*x + n*y + z] += 1 / A_size * B_size

chi2 = sum([(o - e)**2 / e for o, e in zip(O, E)])


print("chi2 of given subset:", chi2)

# Plot colors
#import matplotlib.pyplot as plt
#
#X = np.array([y for x in A for y in x])
#Y = np.array([y for x in B for y in x])
#
#fig = plt.figure()
#
#ax1 = fig.add_subplot(1, 2, 1, projection="3d")
#ax1.scatter(X[:,0], X[:,1], X[:,2], c = X/255)
#
#ax2 = fig.add_subplot(1, 2, 2, projection="3d")
#ax2.scatter(Y[:,0], Y[:,1], Y[:,2], c = Y/255)
#
#plt.show()
