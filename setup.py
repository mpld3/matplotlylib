try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

DESCRIPTION = "Matplotlib to Plotly Converter"
LONG_DESCRIPTION = open('README.md').read()
NAME = "matplotlylib"
AUTHOR = "Andrew Seier"
AUTHOR_EMAIL = "andseier@gmail.com"
MAINTAINER = "Andrew Seier"
MAINTAINER_EMAIL = "andseier@gmail.com"
URL = 'http:/plotly.github.com'
DOWNLOAD_URL = 'https://github.com/plotly/matplotlylib'
LICENSE = 'BSD 3-clause'
VERSION = '0.1'

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=['matplotlylib', 'matplotlylib.mplexporter.mplexporter'])

      # package_data={'mpld3': ['js/*.js']},
      # classifiers=[
      #   'Development Status :: 4 - Beta',
      #   'Environment :: Console',
      #   'Intended Audience :: Science/Research',
      #   'License :: OSI Approved :: BSD License',
      #   'Natural Language :: English',
      #   'Programming Language :: Python :: 2.6'],
     # )