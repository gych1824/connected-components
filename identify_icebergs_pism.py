#!/usr/bin/env python

import cc
import netCDF4 as NC
import numpy as np
import pylab as plt
import argparse

parser = argparse.ArgumentParser()
parser.description = "Identify icebergs using a PISM-style mask read from a file."
parser.add_argument("FILE", nargs=1)
options = parser.parse_args()

nc = NC.Dataset(options.FILE[0])

pism_mask = np.squeeze(nc.variables['mask'][:])
pism_mask_grounded = 2
pism_mask_floating = 3

cc_mask = np.zeros_like(pism_mask)
cc_mask[pism_mask == pism_mask_grounded] = 1
cc_mask[pism_mask == pism_mask_floating] = 2

result = cc.cc(cc_mask, True)               # result is zero everywhere, except 1 if it is an iceberg
result[pism_mask == pism_mask_grounded] = 2 # mark grounded areas

plt.imshow(result, interpolation='nearest')
plt.title("PISM mask read from %s after identifying icebergs" % options.FILE[0])
plt.show()
