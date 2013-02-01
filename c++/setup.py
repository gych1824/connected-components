from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

extra_compile_args=["-O3", "-ffast-math"]

# Define the extension
extension = Extension("cc",
                      sources=["connected_components.cc", "cc.pyx"],
                      include_dirs=[numpy.get_include()],
                      extra_compile_args=extra_compile_args,
                      language="c++")

setup(
    name = "cc",                        # Connected Component Labeling
    version = "0.0.1",
    description = "Connected component labeling",
    long_description = """Uses the standard run-length encoding, 2-scan algorithm
and an array-based implementation of the 'union-find' structure. Includes a modification for
identifying 'icebergs'.""",
    author = "Constantine Khroulev",
    author_email = "ckhroulev@alaska.edu",
    url = "https://github.com/ckhroulev/connected-components",
    cmdclass = {'build_ext': build_ext},
    ext_modules = [extension]
    )
