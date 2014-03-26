=============
matplotlylib:
=============
----------------------------------------------
Sharing matplotlib figures online with plotly.
----------------------------------------------

The Nutshell
~~~~~~~~~~~~

Use this package to render matplotlib figures in plotly. Simply stick a
one-liner in after you've created your mpl figure::

    fig_to_plotly(fig, username, api_key)

That will open up a new browser window with your mpl figure rendererd in
plotly.


About 
~~~~~

Plotly_ is an online collaborative data analysis and graphing tool. The
matplotlylib package allows users to export matplotlib figures to plotly.
Plotly figures are shared, tracked, and edited all online and the data is
always accessible from the graph. The goal of this project is to offer users
a simple interface to send a matplotlib figure to plotly from Python::

    fig_to_plotly(fig, username, api_key)

That's it. Find out more, sign up, and start sharing by visiting us at
https://plot.ly.

Install via pip
~~~~~~~~~~~~~~~

Assuming you have already installed pip, you can simply enter the following
in a terminal program::

    $ pip install matplotlylib

Install via make
~~~~~~~~~~~~~~~~

A makefile is included on the GitHub repo for this project that is not part
of the PyPI distribution. If you want to make changes to this code,
you'll probably want to go this route.

To get started you need to grab a copy of the `matplotlylib repo`_. The
makefile included in this is all you need to get setup. Just do the following::

    $ make build
    $ make install

The first instruction will grab mplexporter and move it into the matplotlylib
directory.

The second instruction will install the matplotlylib package, which now has
mplexporter built into it.

IPython notebook
~~~~~~~~~~~~~~~~

The project page has an extensive `IPython notebook`_ with example usage.

Or, have a look at our `plotly profile`_, where you can open and edit all of
the examples. If the NB is loading slowing, checkout our static site hosted
on GitHub page at: http://plotly.github.io/matplotlylib/.

Details
~~~~~~~

The matplotlylib package requires the matplotlib and plotly Python packages.

This package is based on the mplexporter framework for crawling and exporting
matplotlib images. mplexporter is bundled with the source distribution via
git submodule.

Created by: Plotly_, `@plotlygraphs`_, `matplotlylib@gmail.com`_

License: MIT

.. _Plotly: https://plot.ly
.. _`matplotlylib repo`: https://github.com/mpld3/matplotlylib
.. _`IPython notebook`: http://nbviewer.ipython.org/github/mpld3/matplotlylib/blob/master/notebooks/Plotly%20and%20mpld3.ipynb
.. _`plotly profile`: https://plot.ly/~mpld3/
.. _`@plotlygraphs`: https://twitter.com/plotlygraphs
.. _`matplotlylib@gmail.com`: matplotlylib@gmail.com
