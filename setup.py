#this is a setup.py file
from setuptools import setup, find_packages




VERSION = '1.0.4'
DESCRIPTION = 'Python package for analysis of Multicellular-like phenotype formation in yeast species'
LONG_DESCRIPTION = 'Python package for analysis of Multicellular-like phenotype formation in yeast, for more information see https://github.com/BKover99/yeastmlp'


setup(
    name="yeastmlp",
    version=VERSION,
    author="Bence Kover",
    author_email="<kover.bence@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','scipy', 'scikit-image', 'matplotlib', 'pandas'],
    keywords=['python', 'yeast', 'biology', 'multicellularity', 'adhesion', 'flocculation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

