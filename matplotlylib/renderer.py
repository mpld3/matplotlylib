"""
Plotly Renderer.

A renderer class to be used with an exporter for rendering matplotlib plots
in Plotly.

Attributes:
    PlotlyRenderer -- a renderer class to be used with an Exporter obj
    fig_to_plotly -- a function to send an mpl figure to Plotly

"""
import warnings
from . mplexporter import Exporter, Renderer
from . import tools


class PlotlyRenderer(Renderer):
    """A renderer class inheriting from base for rendering mpl plots in plotly.

    Attributes:
        username -- plotly username, required for fig_to_plotly (default None)
        api_key -- api key for given plotly username (defualt None)
        data -- a list of data dictionaries to be passed to plotly
        layout -- a layout dictionary to be passed to plotly
        axis_ct -- a reference to the number of axes rendered from mpl fig

    Inherited Methods (see renderers.base):
        ax_zoomable(ax) -- static method
        ax_has_xgrid(ax) -- static method
        ax_has_ygrid(ax) -- static method
        current_ax_zoomable(self) -- property
        current_ax_has_xgrid(self) -- property
        current_ax_has_ygrid(self) -- property
        draw_figure(self, fig, props) -- context manager
        draw_axes(self, ax, props) -- context manager

    Reimplemented Methods (see renderers.base):
        open_figure(self, fig, props)
        close_figure(self, fig)
        open_axes(self, ax, props)
        close_axes(self, ax)
        draw_line(self, **props)
        draw_markers(self, **props)
        draw_text(self, **props)

    """
    def __init__(self):
        """Initialize PlotlyRenderer obj.

        PlotlyRenderer obj is called on by an Exporter object to draw
        matplotlib objects like figures, axes, text, etc.

        """
        self.data = []
        self.layout = {}
        self.current_ax_patches = []
        self.axis_ct = 0
        self.mpl_x_bounds = (0, 1)
        self.mpl_y_bounds = (0, 1)

    def open_figure(self, fig, props):
        """Creates a new figure by beginning to fill out layout dict.

        Currently, margins are set to zero to reconcile differences between
        mpl and plotly without complicated transforms. This will be changed
        in future revisions. Autosize is set to false so that the figure will
        mirror sizes set by mpl.

        """
        self.layout['width'] = int(props['figwidth']*props['dpi'])
        self.layout['height'] = int(props['figheight']*props['dpi'])
        self.layout['autosize'] = False
        self.mpl_x_bounds, self.mpl_y_bounds = tools.get_axes_bounds(fig)
        self.layout['margin'] = {
            'l': int(self.mpl_x_bounds[0]*self.layout['width']),
            'r': int((1-self.mpl_x_bounds[1])*self.layout['width']),
            't': int((1-self.mpl_y_bounds[1])*self.layout['height']),
            'b': int(self.mpl_y_bounds[0]*self.layout['height']),
            'pad': 0
        }

    def close_figure(self, fig):
        """Closes figure by cleaning up data and layout dictionaries.

        The PlotlyRenderer's job is to create an appropriate set of data and
        layout dictionaries. When the figure is closed, some cleanup and
        repair is necessary. This method removes inappropriate dictionary
        entries, freeing up Plotly to use defaults and best judgements to
        complete the entries. This method is called by an Exporter object.

        Positional arguments:
        fig -- an mpl figure object.

        """
        tools.repair_data(self.data)
        tools.repair_layout(self.layout)
        for data_dict in self.data:
            tools.clean_dict(data_dict)
        try:
            for annotation_dict in self.layout['annotations']:
                tools.clean_dict(annotation_dict)
        except KeyError:
            pass
        tools.clean_dict(self.layout)
        self.layout['showlegend'] = False

    def open_axes(self, ax, props):
        """Setup a new axes object (subplot in plotly).

        Plotly stores information about subplots in different 'xaxis' and
        'yaxis' objects which are numbered. These are just dictionaries
        included in the layout dictionary. This function takes information
        from the Exporter, fills in appropriate dictionary entries,
        and updates the layout dictionary. PlotlyRenderer keeps track of the
        number of plots by incrementing the axis_ct attribute.

        Setting the proper plot domain in plotly is a bit tricky. Refer to
        the documentation for tools.get_plotly_x_domain and
        tools.get_plotly_y_domain.

        Positional arguments:
        ax -- an mpl axes object. This will become a subplot in plotly.
        props -- selected axes properties from the exporter (a dict).

        """
        self.axis_ct += 1
        layout = {
            'xaxis{}'.format(self.axis_ct): {
                'range': props['xlim'],
                'showgrid': props['axes'][1]['grid']['gridOn'],
                'domain': tools.get_plotly_x_domain(props['bounds'],
                                                           self.mpl_x_bounds),
                'anchor': 'y{}'.format(self.axis_ct),
                'zeroline': False
            },
            'yaxis{}'.format(self.axis_ct): {
                'range': props['ylim'],
                'showgrid': props['axes'][0]['grid']['gridOn'],
                'domain': tools.get_plotly_y_domain(props['bounds'],
                                                           self.mpl_y_bounds),
                'anchor': 'x{}'.format(self.axis_ct),
                'zeroline': False
            }
        }
        for key, value in layout.items():
            self.layout[key] = value

    def close_axes(self, ax):
        """Close the axes object and clean up.

        Bars from bar charts are given to PlotlyRenderer one-by-one,
        thus they need to be taken care of at the close of each axes object.
        The self.current_ax_patches variable should be empty unless a bar
        chart has been created or a rectangle object has been drawn that has
        an edge exactly on the lines x=0 or y=0.

        Positional arguments:
        ax -- an mpl axes object, not required at this time.

        """
        for patch_coll in self.current_ax_patches:
            self.draw_bar(patch_coll)
        self.current_ax_patches = []  # clear this for next axes obj

    def draw_bar(self, patch_coll):
        """Draw a collection of similar patches as a bar chart.

        After bars are sorted, an appropriate data dictionary must be created
        to tell plotly about this data. Just like draw_line or draw_markers,
        draw_bar translates patch/path information into something plotly
        understands.

        Positional arguments:
        patch_coll -- a collection of patches to be drawn as a bar chart.

        """
        bardir = patch_coll[0]['bardir']
        if bardir == 'v':
            patch_coll.sort(key=lambda b: b['x0'])
            data = {
                'type': 'bar',
                'bardir': bardir,
                'x': [bar['x0']+(bar['x1']-bar['x0'])/2
                      for bar in patch_coll],
                'y': [bar['y1'] for bar in patch_coll],
                'xaxis': 'x{}'.format(self.axis_ct),
                'yaxis': 'y{}'.format(self.axis_ct),
                'marker': {
                    'color': patch_coll[0]['facecolor'],
                    'line': {
                        'width': patch_coll[0]['edgewidth']
                    }
                },
                'opacity': patch_coll[0]['alpha']
            }
        elif bardir == 'h':
            patch_coll.sort(key=lambda b: b['y0'])
            data = {
                'type': 'bar',
                'bardir': bardir,
                'x': [bar['y0']+(bar['y1']-bar['y0'])/2
                      for bar in patch_coll],
                'y': [bar['x1'] for bar in patch_coll],
                'xaxis': 'x{}'.format(self.axis_ct),
                'yaxis': 'y{}'.format(self.axis_ct),
                'marker': {
                    'color': patch_coll[0]['facecolor'],
                    'line': {
                        'width': patch_coll[0]['edgewidth']
                    }
                },
                'opacity': patch_coll[0]['alpha']
            }
        if len(data['x']) > 1:
            self.data += data,
        else:
            warnings.warn('found box chart data with length <= 1, '
                          'assuming data redundancy, not plotting.')

    def draw_line(self, **props):
        """Create a data dict for a line obj.

        Props dict (key: value):
        'coordinates': 'data', 'axes', 'figure', or 'display'.
        'data': a list of xy pairs.
        'style': style dict from utils.get_line_style
        'mplobj': an mpl object, in this case the line object.

        """
        if props['coordinates'] == 'data':
            trace = {
                'mode': 'lines',
                'x': [xy_pair[0] for xy_pair in props['data']],
                'y': [xy_pair[1] for xy_pair in props['data']],
                'xaxis': 'x{}'.format(self.axis_ct),
                'yaxis': 'y{}'.format(self.axis_ct),
                'line': {
                    'opacity': props['style']['alpha'],
                    'color': props['style']['color'],
                    'width': props['style']['linewidth'],
                    'dash': tools.convert_dash(props['style'][
                        'dasharray'])
                }
            }
            self.data += trace,
        else:
            pass

    def draw_markers(self, **props):
        """Create a data dict for a line obj using markers.

        Props dict (key: value):
        'coordinates': 'data', 'axes', 'figure', or 'display'.
        'data': a list of xy pairs.
        'style': style dict from utils.get_marker_style
        'mplobj': an mpl object, in this case the line object.

        """
        if props['coordinates'] == 'data':
            trace = {
                'mode': 'markers',
                'x': [xy_pair[0] for xy_pair in props['data']],
                'y': [xy_pair[1] for xy_pair in props['data']],
                'xaxis': 'x{}'.format(self.axis_ct),
                'yaxis': 'y{}'.format(self.axis_ct),
                'marker': {
                    'opacity': props['style']['alpha'],
                    'color': props['style']['facecolor'],
                    'symbol': tools.convert_symbol(props['style'][
                        'marker']),
                    'line': {
                        'color': props['style']['edgecolor'],
                        'width': props['style']['edgewidth']
                    }
                }
            }
            if 'markersize' in props['style']:
                trace['marker']['size'] = props['style']['markersize']
            # not sure whether we need to incorporate style['markerpath']
            self.data += trace,
        else:
            pass

    def draw_image(self, **props):
        """Draw image.

        Not implemented yet!

        """
        warnings.warn('draw_image not implemented yet, images will not show '
                      'up in plotly.')

    def draw_path_collection(self, paths, path_coordinates, path_transforms,
                             offsets, offset_coordinates, offset_order,
                             styles, mplobj=None):
        """Add a path collection to data list as a scatter plot.

        Current implementation defaults such collections as scatter plots.

        """
        if offset_coordinates is 'data':
            alpha_face = styles['facecolor'][0][3]
            rgb_face = [int(c*255) for c in styles['facecolor'][0][:3]]
            alpha_edge = styles['edgecolor'][0][3]
            rgb_edge = [int(c*255) for c in styles['edgecolor'][0][:3]]
            data = offsets
            marker = tools.path_to_mpl_symbol(paths[0])
            style = {
                'alpha': alpha_face,
                'facecolor': 'rgb({},{},{})'.format(*rgb_face),
                'marker': marker,
                'edgecolor': 'rgb({},{},{})'.format(*rgb_edge),
                'edgewidth': styles['linewidth'][0],
                'markersize': tools.get_marker_size(
                    dpi=self._current_fig.get_dpi(), aff=path_transforms[0])
            }
            props = {
                'coordinates': 'data',
                'data': data,
                'style': style,
            }
            self.draw_markers(**props)
        else:
            warnings.warn('path collection is not linked to data, implemented '
                          'of such path collections is not yet supported.')

    def draw_path(self, **props):
        """Draw path, currently only attempts to draw bar charts.

        This function attempts to sort a given path into a collection of
        horizontal or vertical bar charts. Most of the actual code takes
        place in functions from tools.py.

        """
        is_bar = tools.is_bar(**props)
        is_barh = tools.is_barh(**props)
        if is_bar:  # if we think it's a bar, add it!
            bar = tools.make_bar(bardir='v', **props)
            self.file_bar(bar)
        if is_barh:  # perhaps a horizontal bar?
            bar = tools.make_bar(bardir='h', **props)
            self.file_bar(bar)
        if not (is_bar or is_barh):
            warnings.warn("I found a path object that I don't think is part "
                          "of a bar chart. Ignoring...")

    def file_bar(self, bar):
        """Puts a given bar into an appropriate bar or barh collection.

        Bars come from the mplexporter one-by-one. To try to put them into
        appropriate data sets, we must compare them to existing data.

        Positional arguments:
        bar -- a bar dictionary created in tools.make_bar.py.

        """
        if len(self.current_ax_patches) == 0:
            self.current_ax_patches.append([])
            self.current_ax_patches[-1] += bar,
        else:
            match = False
            for patch_collection in self.current_ax_patches:
                if tools.check_bar_match(patch_collection[0], bar):
                    match = True
                    patch_collection += bar,
            if not match:
                self.current_ax_patches.append([])
                self.current_ax_patches[-1] += bar,

    def draw_text(self, **props):
        """Create an annotation dict for a text obj.

        Currently, plotly uses either 'page' or 'data' to reference
        annotation locations. These refer to 'display' and 'data',
        respectively for the 'coordinates' key used in the Exporter.
        Appropriate measures are taken to transform text locations to
        reference one of these two options.

        Props dict (key: value):
        'coordinates': reference for position, 'data', 'axes', 'figure', etc.
        'position': x,y location of text in the given coordinates.
        'style': style dict from utils.get_text_style.
        'text': actual string content.

        """
        if 'annotations' not in self.layout:
            self.layout['annotations'] = []
        if props['text_type'] == 'xlabel':
            self.draw_xlabel(**props)
        elif props['text_type'] == 'ylabel':
            self.draw_ylabel(**props)
        elif props['text_type'] == 'title':
            self.draw_title(**props)
        else:  # just a regular text annotation...
            if props['coordinates'] is not 'data':
                x_px, y_px = props['mplobj'].get_transform().transform(
                    props['position'])
                x, y = tools.convert_to_paper(x_px, y_px, self.layout)
                xref = 'paper'
                yref = 'paper'
                xanchor = props['style']['halign']  # no difference here!
                yanchor = tools.convert_va(props['style']['valign'])
            else:
                x, y = props['position']
                xref = 'x{}'.format(self.axis_ct)
                yref = 'y{}'.format(self.axis_ct)
                xanchor = 'center'
                yanchor = 'middle'
            annotation = {
                'text': props['text'],
                'opacity': props['style']['alpha'],
                'x': x,
                'y': y,
                'xref': xref,
                'yref': yref,
                'xanchor': xanchor,
                'yanchor': yanchor,
                'font': {'color': props['style']['color'],
                         'size': props['style']['fontsize']
                },
                'showarrow': False  # change this later?
            }
            self.layout['annotations'] += annotation,

    def draw_title(self, **props):
        """Add a title to the current subplot in layout dictionary.

        If there exists more than a single plot in the figure, titles revert
        to 'page'-referenced annotations.

        """
        if len(self._current_fig.axes) > 1:
            x_px, y_px = props['mplobj'].get_transform().transform(props[
                'position'])
            x, y = tools.convert_to_paper(x_px, y_px, self.layout)
            annotation = {
                'text': props['text'],
                'font': {'color': props['style']['color'],
                         'size': props['style']['fontsize']
                },
                'xref': 'paper',
                'yref': 'paper',
                'x': x,
                'y': y,
                'xanchor': 'center',
                'yanchor': 'bottom',
                'showarrow': False  # no arrow for a title!
            }
            self.layout['annotations'] += annotation,
        else:
            self.layout['title'] = props['text']
            titlefont = {'size': props['style']['fontsize'],
                         'color': props['style']['color']
            }
            self.layout['titlefont'] = titlefont

    def draw_xlabel(self, **props):
        """Add an xaxis label to the current subplot in layout dictionary."""
        self.layout['xaxis{}'.format(self.axis_ct)]['title'] = props['text']
        titlefont = {'size': props['style']['fontsize'],
                     'color': props['style']['color']
        }
        self.layout['xaxis{}'.format(self.axis_ct)]['titlefont'] = titlefont

    def draw_ylabel(self, **props):
        """Add a yaxis label to the current subplot in layout dictionary."""
        self.layout['yaxis{}'.format(self.axis_ct)]['title'] = props['text']
        titlefont = {'size': props['style']['fontsize'],
                     'color': props['style']['color']
        }
        self.layout['yaxis{}'.format(self.axis_ct)]['titlefont'] = titlefont

    def resize(self):
        """Revert figure layout to allow plotly to resize.

        By default, PlotlyRenderer tries its hardest to precisely mimic an
        mpl figure. However, plotly is pretty good with aesthetics. By
        running PlotlyRenderer.resize(), layout parameters are deleted. This
        lets plotly choose them instead of mpl.

        """
        for key in ['width', 'height', 'autosize', 'margin']:
            try:
                del self.layout[key]
            except KeyError:
                pass

    def strip_style(self):
        for data_dict in self.data:
            tools.walk_and_strip(data_dict, tools.SAFE_KEYS[
               'data'])
            tools.clean_dict(data_dict)
        tools.walk_and_strip(self.layout, tools.SAFE_KEYS[
            'layout'])
        tools.clean_dict(self.layout)
        try:
            for annotation in self.layout['annotations']:
                tools.clean_dict(annotation)
        except KeyError:
            pass  # guess there weren't any annotations...


def fig_to_plotly(fig, username=None, api_key=None, notebook=False,
                  resize=False, strip_style=False):
    """Convert a matplotlib figure to plotly dictionary and send.

    All available information about matplotlib visualizations are stored
    within a matplotlib.figure.Figure object. You can create a plot in python
    using matplotlib, store the figure object, and then pass this object to
    the fig_to_plotly function. In the background, mplexporter is used to
    crawl through the mpl figure object for appropriate information. This
    information is then systematically sent to the PlotlyRenderer which
    creates the JSON structure used to make plotly visualizations. Finally,
    these dictionaries are sent to plotly and your browser should open up a
    new tab for viewing! Optionally, if you're working in IPython, you can
    set notebook=True and the PlotlyRenderer will call plotly.iplot instead
    of plotly.plot to have the graph appear directly in the IPython notebook.

    Note, this function gives the user access to a simple, one-line way to
    render an mpl figure in plotly. If you need to trouble shoot, you can do
    this step manually by NOT running this fuction and entereing the following:

    ============================================================================
    from mplexporter import Exporter
    from mplexporter.renderers import PlotlyRenderer

    # create an mpl figure and store it under a varialble 'fig'

    renderer = PlotlyRenderer()
    exporter = Exporter(renderer)
    exporter.run(fig)
    ============================================================================

    You can then inspect the JSON structures by accessing these:

    renderer.layout -- a plotly layout dictionary
    renderer.data -- a list of plotly data dictionaries

    Positional arguments:
    fig -- a matplotlib figure object
    username -- a valid plotly username **
    api_key -- a valid api_key for the above username **
    notebook -- an option for use with an IPython notebook

    ** Don't have a username/api_key? Try looking here:
    https://plot.ly/plot

    ** Forgot your api_key? Try signing in and looking here:
    https://plot.ly/api/python/getting-started

    """
    import plotly
    renderer = PlotlyRenderer()
    Exporter(renderer).run(fig)
    if resize:
        renderer.resize()
    if strip_style:
        renderer.strip_style()
    py = plotly.plotly(username, api_key)
    if notebook:
        return py.iplot(renderer.data, layout=renderer.layout)
    else:
        py.plot(renderer.data, layout=renderer.layout)
