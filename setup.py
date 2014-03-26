try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

exec(open('matplotlylib/version.py').read())

setup(name='matplotlylib',
      version=__version__,
      description="Matplotlib to Plotly Converter",
      long_description=open('README.rst').read(),
      author="Andrew Seier",
      author_email="andseier@gmail.com",
      install_requires=['plotly', 'matplotlib'],
      maintainer="Andrew Seier",
      maintainer_email="andseier@gmail.com",
      url='http:/mpld3.github.com',
      download_url='https://github.com/mpld3/'
                   'matplotlylib/tarball/{}'.format(__version__),
      license='MIT',
      packages=['matplotlylib',
                'matplotlylib/mplexporter',
                'matplotlylib/mplexporter/renderers'])
