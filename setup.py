"""
Setup configuration to be able to build an official package for PyPi.

"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blueliv-api",
    version="1.0.1",
    author="Román Ramírez",
    author_email="rramirez@rootedcon.com",
    description="Blueliv's API encapsulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patowc/blueliv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT'
)
