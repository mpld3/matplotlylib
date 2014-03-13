# matplotlylib:


### Sharing matplotlib figures online with plotly
------------------------------

About 
-----

Plotly is a collaborative data analysis and graphing tool. The matplotlylib package allows users to take matplotlib figures and upload them to plotly where the data is linked directly to the graph and figures can be shared, tracked, and edited.

Find out more, sign up, and start sharing by [visiting us](https://plot.ly/).

Install
-------
matplotlylib requires the [matplotlib](http://matplotlib.org)  and [plotly](https://github.com/plotly/python-api) Python packages.

This package is based on the [mplexporter](http://github.com/mpld3/mplexporter) framework for crawling and exporting matplotlib images. mplexporter is bundled with the source distribution via git submodule.

To get started you need to grab a copy of the matplotlylib repo. The makefile included in this is all you need to get setup. Just do the following:

1. $ make build

2. $ make install

The first instruction will grab mplexporter and move it into the matplotlylib directory.

The second instruction will install the matplotlylib package, which now has mplexporter built into it.

Gallery
-------
Check out the [IPython Notebook](http://nbviewer.ipython.org/github/mpld3/matplotlylib/blob/master/notebooks/Plotly%20and%20mpld3.ipynb), or have a look at our [plotly profile](https://plot.ly/~mpld3/) where you can open and edit all of the examples.

### Lines
---------
![](gallery/lines.png)

### Bars
--------
![](gallery/bars.png)

### Scatter
-----------
![](gallery/scatter.png)

### Subplots
------------
![](gallery/subplots.png)

### Annotations
---------------
![](gallery/annotations.png)

Details
-------
Created by: Plotly <matplotlylib@gmail.com>

License: BSD 3-clause
