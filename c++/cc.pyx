# -*- mode: cython -*-
cimport numpy as np
cimport connected_components

ctypedef np.float64_t double_t

def cc(np.ndarray[dtype=double_t, ndim=2, mode='c'] image, identify_icebergs=False, mask_grounded=1):
    """
    result = cc(image)

    Labels connected components in a binary image `image`. Pixels with the value of 0
    are background, pixels with values greater than zero -- foreground.
    """
    cdef np.ndarray[dtype=double_t, ndim=2, mode='c'] result
    cdef unsigned int n_rows, n_cols

    result = image.copy()
    n_rows = image.shape[0]
    n_cols = image.shape[1]

    connected_components.cc(<double*>result.data, n_rows, n_cols, identify_icebergs, mask_grounded)

    return result
