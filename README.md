This is an implementation of the standard 2-scan connected component labeling algorithm using run-length encoding.

It includes a modification for identifying "icebergs". In this context an "iceberg" is a component (blob with a positive mask value) that does not contain any "grounded" points.

![figure](https://raw.github.com/ckhroulev/connected-components/master/figure.png)
