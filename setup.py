from setuptools import setup, find_packages
import gfa

setup(
    name="gfautils",
    version=gfa.__version__,
    packages=find_packages()
)

