from setuptools import setup
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(name='orion',
      version='1.0.0',
      description='Performance Test Framework',
      classifiers=[
          'Programming Language :: Python :: 3.6.3',
      ],
      packages=['orion.core', 'orion.utils', 'orion.'],
      package_dir={'': 'src'},
      install_requires=REQUIREMENTS,
      scripts=['bin/orion_run']
      )
