from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("table_model.pyx", language_level=3)
)
