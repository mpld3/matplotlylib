all : build

sync_current : mplexporter
	rsync -r mplexporter/mplexporter matplotlylib/

sync_submodule : mplexporter
	git submodule init
	git submodule update
	rsync -r mplexporter/mplexporter matplotlylib/

build : sync_submodule sync_current
	python setup.py build

install : build
	python setup.py install
