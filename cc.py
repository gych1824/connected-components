#!/usr/bin/env python

def cc(input, identify_icebergs=False, mask_grounded=1):
    image = input.copy()
    n_rows, n_cols = image.shape

    # Add one "dummy" run. This is so that the first actual run uses index==1
    # and 0 (background) is not the index of any run.
    parents = [0]
    rows    = [0]
    columns = [0]
    lengths = [0]
    mask    = [0]                       # floating=0/grounded=1 mask (for each run)

    def run_union(run1, run2):
        """Joins trees runs 'run1' and 'run2' are parts of."""

        # Trivial case: merging a run with the one right below it.
        if parents[run1] == run2 or parents[run2] == run1:
            return

        while parents[run1] != 0:
            run1 = parents[run1]

        while parents[run2] != 0:
            run2 = parents[run2]

        # These if conditions ensure that the parent of a run has the
        # index smaller than indices of all children.
        # This makes it easier to compute final labels (see below).
        if run1 > run2:
            parents[run1] = run2
        elif run1 < run2:
            parents[run2] = run1
        else:
            pass

    # First scan
    run_number = 0
    for r in xrange(n_rows):
        for c in xrange(n_cols):
            if image[r,c] > 0:             # foreground pixel
                if c > 0 and image[r,c-1] > 0:
                    # one to the left is also foreground: continue the run
                    lengths[run_number] += 1
                else:
                    # one to the left is a background pixel (or this is column 0): start a new run

                    # check the pixel above and set the parent
                    if r > 0 and image[r-1,c] > 0:
                        parent = int(image[r-1,c])
                    else:
                        parent = 0

                    run_number += 1
                    rows.append(r)
                    columns.append(c)
                    parents.append(parent)
                    lengths.append(1)
                    mask.append(0)

                if r > 0 and image[r-1,c] > 0:
                    run_union(int(image[r-1,c]), run_number)

                # if a run if known as "floating" and the current pixel is "grounded", mark
                # the whole run as "grounded"
                if mask[run_number] == 0 and image[r,c] == mask_grounded:
                    mask[run_number] = 1

                image[r,c] = run_number
            else:
                pass

    # Assign labels to runs
    # This uses the fact that children always follow parents in 'runs',
    # so we can do just one sweep: by the time we get to a node (run),
    # its parent already has a final label.
    #
    # We use "parents" to store labels here, because once a label is computed
    # we don't need to know the parent of a run any more.

    grounded = []
    label = 0                           # this label is used for the dummy run
    for k in xrange(run_number + 1):
        if parents[k] == 0:
            parents[k] = label
            label += 1
            grounded.append(0)
        else:
            parents[k] = parents[parents[k]]

        # remember current blob (parents[k]) as "grounded" if the current run is
        # "grounded"
        if mask[k] == 1:
            grounded[parents[k]] = 1

    # Second scan (re-label)
    if identify_icebergs:
        # identify icebergs (iceberg=1, grounded=2)
        for k in xrange(run_number + 1):
            for n in xrange(lengths[k]):
                image[rows[k], columns[k] + n] = 1 - grounded[parents[k]]
    else:
        # just label blobs
        for k in xrange(run_number + 1):
            for n in xrange(lengths[k]):
                image[rows[k], columns[k] + n] = parents[k]

    return image
