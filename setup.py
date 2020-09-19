#!/usr/bin/env python 

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfabots", # Replace with your own username
    version="0.0.1",
    author="CFA Team",
    author_email="miguelhinojosa994@gmail.com",
    description="Post SisPI outputs and information on social media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MigueLesPaul/cfabots",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=('facebook-sdk','telepot'),
)