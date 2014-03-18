"""
plotly_objs
===========

A module that understands plotly language and can deal manage the json
structures.

"""

from . plotly_words import *


class PlotlyList(list):
    """
    A container for PlotlyDicts, inherits from standard list.

    Plotly uses lists and dicts as collections to hold information about a
    figure. This container is simply a list that understands some plotly
    language and apes the methods in a PlotlyDict, passing them on to its
    constituents.

    It can be initialized like any other list so long as the entries are all
    PlotlyDict objects or subclasses thereof.

    Any available methods that hold for a list object hold for a PlotlyList.

    """
    def __init__(self, *args):
        """Initialize PlotlyList.

        Differs from list initialization only in that it forces all new items
        to be added through the `append`.

        Positional arguments:
        args -- a list of positional arguments of any length

        """
        for arg in args:
            self.append(arg)

    def __setitem__(self, key, value):
        if not isinstance(value, PlotlyDict):
            raise ValueError("Only PlotlyDict or subclasses thereof can "
                             "populate a PlotlyList.")
        super(PlotlyList, self).__setitem__(key, value)

    def append(self, arg):
        if not isinstance(arg, PlotlyDict):
            raise ValueError("Only PlotlyDict or subclasses thereof can "
                             "populate a PlotlyList.")
        super(PlotlyList, self).append(arg)

    def get_json(self):
        """Return a json structure representation for the PlotlyList."""
        l = list()
        for pd in self:
            l.append(pd.get_json())
        return l

    def strip(self):
        """Strip style information from each of the PlotlyList's entries."""
        for pd in self:
            pd.strip()

    def clean(self):
        """Remove any entries that are NoneType from PlotlyLists's entries."""
        for item in self:
            item.clean()

    def check(self):
        """Check each entry in the PlotlyList for invalid keys."""
        for item in self:
            item.check()

    def repair_vals(self):
        """Some unfortunately placed functionality for use with mplexporter."""
        for item in self:
            item.repair_vals()

    def repair_keys(self):
        """Some unfortunately placed functionality for use with mplexporter."""
        for item in self:
            item.repair_keys()


class PlotlyDict(dict):
    """A base class for all objects that style a figure in plotly.

    A PlotlyDict can be instantiated like any dict object. This class offers
    some useful recursive methods that can be used by higher-level subclasses
    and containers so long as all plot objects are instantiated as a subclass
    of PlotlyDict.

    Any available methods that hold for a dict hold for a PlotlyDict.

    """
    def __init__(self, _safe_keys=[], _valid_keys=[],
                 _repair_keys={}, _repair_vals={} , **kwargs):
        kwargs['_safe_keys'] = _safe_keys
        kwargs['_valid_keys'] = _valid_keys
        kwargs['_repair_keys'] = _repair_keys
        kwargs['_repair_vals'] = _repair_vals
        super(PlotlyDict, self).__init__(**kwargs)

    def __str__(self):
        return str(self.get_json())

    def _pop_keys(self):
        """Remove non-functional keys from PlotlyDict.

        This is only temporary and should be used only by the PlotlyDict class.

        """
        return [self.pop('_safe_keys'), self.pop('_valid_keys'),
                self.pop('_repair_keys'), self.pop('_repair_vals')]

    def _push_keys(self, _safe_keys, _valid_keys, _repair_keys, _repair_vals):
        """Add non-functional keys back to PlotlyDict.

        This is only temporary and should be used only by the PlotlyDict class.

        """
        self['_safe_keys'], self['_valid_keys'] = _safe_keys, _valid_keys
        self['_repair_keys'], self['_repair_vals'] = _repair_keys, _repair_vals

    def get_json(self):
        """Get a JSON representation for the PlotlyDict.

        This function changes all of the internal PlotlyDicts and PlotlyLists
        into normal lists and dicts. Though duck-typing should allow
        PlotlyLists and PlotlyDicts to be sent to plotly directly, this is a
        safer approach for compatibility.

        """
        d = dict()
        _safe_keys, _valid_keys, _repair_keys, _repair_vals = self._pop_keys()
        for key, val in self.items():
            try:
                d[key] = val.get_json()
            except AttributeError:
                d[key] = val
        self._push_keys(_safe_keys, _valid_keys, _repair_keys, _repair_vals)
        return d

    def strip(self):
        """Strip style from the current representation of the plotly figure.

        All PlotlyDicts and PlotlyLists are guaranteed to survive the
        stripping process, though they made be left empty. This is allowable.
        The other attributes that will not be deleted are stored in the
        plotly_words module under *_SAFE_KEYS.

        """
        _safe_keys, _valid_keys, _repair_keys, _repair_vals = self._pop_keys()
        keys = self.keys()
        for key in keys:
            try:
                self[key].strip()
            except AttributeError:
                if key not in _safe_keys:
                    del self[key]
        self._push_keys(_safe_keys, _valid_keys, _repair_keys, _repair_vals)

    def clean(self):
        """Recursively rid PlotlyDict of `None` entries.

        This only rids a PlotlyDict of `None` entries, not empty dictionaries or
        lists.

        """
        del_keys = [key for key in self if self[key] is None]
        for key in del_keys:
            del self[key]
        for val in self.values():
            try:
                val.clean()
            except AttributeError:
                pass

    def check(self):
        """Recursively check the validity of the keys in a PlotlyDict.

        The valid keys are stored in plotly_word.py under *_VALID_KEYS for
        each plotly object.

        """
        _safe_keys, _valid_keys, _repair_keys, _repair_vals = self._pop_keys()
        for key, val in self.items():
            try:
                val.check()
            except AttributeError:
                if key not in _valid_keys:
                    raise KeyError("Invalid key, {}, for type {}".format(
                        key, type(self)))
        self._push_keys(_safe_keys, _valid_keys, _repair_keys, _repair_vals)

    def repair_vals(self):
        """Repair known common value problems.

        Plotly objects that require this functionality define a private
        `_repair_vals` dictionary at the top of the class. The structure of
        these dictionaries are as follows:

        _repair_vals = dict(key_1=[suspect_val_1, correct_val_1], ...)

        """
        for key in self:
            try:
                self[key].repair_vals()
            except AttributeError:
                try:
                    if self[key] == self['_repair_vals'][key][0]:
                        self[key] = self['_repair_vals'][key][1]
                except KeyError:
                    pass
        self.clean()

    def repair_keys(self):
        """Repair known common key problems.

        Plotly objects that require this functionality define a private
        `_repair_keys` dictionary at the top of the class. The structure of
        these dictionaries are as follows:

        _repair_keys = dict(suspect_key_1=correct_key_1, ...)

        """
        for key in self:
            if key in self['_repair_keys']:
                self[self['_repair_keys'][key]] = self.pop(key)
        for key in self:
            try:
                self[key].repair_keys()
            except AttributeError:
                pass
        self.clean()


class Data(PlotlyDict):
    """A general data class for plotly.

    This class is meant to hold any type of allowable plotly data.

    """
    _repair_vals = dict(xaxis=['x1', None], yaxis=['y1', None])

    def __init__(self, **kwargs):
        super(Data, self).__init__(_safe_keys=DATA_SAFE_KEYS,
                                   _valid_keys=DATA_VALID_KEYS,
                                   _repair_vals=Data._repair_vals, **kwargs)


class Marker(PlotlyDict):
    """A marker class for creating markers on plots."""
    def __init__(self, **kwargs):
        super(Marker, self).__init__(_safe_keys=MARKER_SAFE_KEYS,
                                     _valid_keys=MARKER_VALID_KEYS, **kwargs)


class Annotation(PlotlyDict):
    """An annotation holder for making notes on figures."""
    pass


class Line(PlotlyDict):
    """A line class for scatter lines or marker lines."""
    def __init__(self, **kwargs):
        super(Line, self).__init__(_safe_keys=LINE_SAFE_KEYS,
                                   _valid_keys=LINE_VALID_KEYS, **kwargs)


class Layout(PlotlyDict):
    """A layout class for holding figure layout information."""
    _repair_keys = dict(xaxis1='xaxis', yaxis1='yaxis')

    def __init__(self, **kwargs):
        super(Layout, self).__init__(_safe_keys=LAYOUT_SAFE_KEYS,
                                     _valid_keys=LAYOUT_VALID_KEYS,
                                     _repair_keys=Layout._repair_keys, **kwargs)


class DataList(PlotlyList):
    """A simple list container for holding Data objects."""
    pass


class AnnotationList(PlotlyList):
    """A simple list container for holding Annotation objects."""
    pass


class Annotation(PlotlyDict):
    """An dictionary for and annotation, note, to be placed on a figure."""
    _repair_vals = dict(xref=['x1', 'x'], yref=['y1', 'y'])

    def __init__(self, **kwargs):
        super(Annotation, self).__init__(_safe_keys=ANNOTATION_SAFE_KEYS,
                                         _valid_keys=ANNOTATION_VALID_KEYS,
                                         _repair_vals=Annotation._repair_vals,
                                         **kwargs)


class XAxis(PlotlyDict):
    """An xaxis object to be used in a Layout object."""
    _repair_vals = dict(anchor=['y1', 'y'])

    def __init__(self, **kwargs):
        super(XAxis, self).__init__(_safe_keys=XAXIS_SAFE_KEYS,
                                    _valid_keys=XAXIS_VALID_KEYS,
                                    _repair_vals=XAxis._repair_vals, **kwargs)


class YAxis(PlotlyDict):
    """An xaxis object to be used in a Layout object."""
    _repair_vals = dict(anchor=['x1', 'x'])

    def __init__(self, **kwargs):
        super(YAxis, self).__init__(_safe_keys=YAXIS_SAFE_KEYS,
                                    _valid_keys=YAXIS_VALID_KEYS,
                                    _repair_vals=YAxis._repair_vals, **kwargs)


class Margin(PlotlyDict):
    """An object to contain figure margin information."""

    def __init__(self, **kwargs):
        super(Margin, self).__init__(_safe_keys=MARGIN_SAFE_KEYS,
                                     _valid_keys=MARGIN_VALID_KEYS, **kwargs)


class Font(PlotlyDict):
    """A general font class for storing font information."""
    def __init__(self, **kwargs):
        super(Font, self).__init__(_safe_keys=FONT_SAFE_KEYS,
                                   _valid_keys=FONT_VALID_KEYS, **kwargs)


class Legend(PlotlyDict):
    """An object to contain legend information for a figure."""
    pass


class PlotlyFig(object):
    """An experimental interface for adding data and format information."""
    def __init__(self, data=None, layout=None):
        if isinstance(data, PlotlyList):
            self.data = data
        elif isinstance(data, PlotlyDict):
            self.data = PlotlyList(data)
        elif isinstance(data, (dict, type(None))):
            self.data = Data(data)
        else:
            raise ValueError("data must be a PlotlyList, PlotlyDict, dict, "
                             "or None")
        if isinstance(layout, Layout):
            self.layout = layout
        elif isinstance(layout, (dict, type(None))):
            self.layout = Layout(layout)
        else:
            raise ValueError("layout must be a Layout, dict, or None")

    def add_line(self, data):
        """Not yet implemented."""
        pass

    def add_bar(self, data):
        """Not yet implemented."""
        pass

    def __str__(self):
        """Not yet implemented."""
        pass
