import numpy as np
import sys

def reshaper(outname,inpname):
    inpvar = np.load(inpname)
    x, three_y = inpvar.shape
    y = three_y // 3
    outvar = inpvar.reshape((x, y, 3))

np.save('new_'+sys.argv[1], sys.argv[1])


