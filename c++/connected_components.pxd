# -*- mode: cython -*-

cdef extern from "connected_components.hh":
     void cc(double *image, unsigned int n_rows, unsigned int n_cols, bint identify_icebergs, double mask_grounded)

