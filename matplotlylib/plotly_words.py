"""
plotly_words
============

A module that contains language data for plotly. There is not meant to be
functionality here, only some definitions for use with the plotly_words module.

"""

DATA_VALID_KEYS = [
    'textfont',
    'name',
    'marker',
    'mode',
    'y',
    'x',
    'line',
    'type',
    'error_y',
    'opacity',
    'bardir'
]

DATA_SAFE_KEYS = [
    'name',
    'y',
    'x',
    'type',
    'bardir'
]

LAYOUT_VALID_KEYS = [
    'title',
    'xaxis',
    'yaxis',
    'legend',
    'width',
    'height',
    'autosize',
    'margin',
    'paper_bgcolor',
    'plot_bgcolor',
    'barmode',
    'bargap',
    'bargroupgap',
    'boxmode',
    'boxgap',
    'boxgroupgap',
    'font',
    'titlefont',
    'dragmode',
    'hovermode',
    'separators',
    'hidesources',
    'showlegend',
    'annotations'
]

LAYOUT_SAFE_KEYS = [
    'title',
    'width',
    'height',
    'autosize'
]

XAXIS_VALID_KEYS = [
    'range',
    'type',
    'showline',
    'mirror',
    'linecolor',
    'linewidth',
    'tick0',
    'dtick',
    'ticks',
    'ticklen',
    'tickcolor',
    'nticks',
    'showticklabels',
    'tickangle',
    'exponentformat',
    'showexponent',
    'showgrid',
    'gridcolor',
    'gridwidth',
    'autorange',
    'rangemode',
    'autotick',
    'zeroline',
    'zerolinecolor',
    'zerolinewidth',
    'titlefont',
    'tickfont',
    'overlaying',
    'domain',
    'position',
    'anchor',
    'title'
]

XAXIS_SAFE_KEYS = [
    'range',
    'type',
    'showticklabels',
    'exponentformat',
    'zeroline',
    'overlaying',
    'domain',
    'position',
    'anchor',
    'title'
]

YAXIS_VALID_KEYS = [
    'range',
    'type',
    'showline',
    'mirror',
    'linecolor',
    'linewidth',
    'tick0',
    'dtick',
    'ticks',
    'ticklen',
    'tickcolor',
    'nticks',
    'showticklabels',
    'tickangle',
    'exponentformat',
    'showexponent',
    'showgrid',
    'gridcolor',
    'gridwidth',
    'autorange',
    'rangemode',
    'autotick',
    'zeroline',
    'zerolinecolor',
    'zerolinewidth',
    'titlefont',
    'tickfont',
    'overlaying',
    'domain',
    'position',
    'anchor',
    'title'
]

YAXIS_SAFE_KEYS = [
    'range',
    'type',
    'showticklabels',
    'exponentformat',
    'zeroline',
    'overlaying',
    'domain',
    'position',
    'anchor',
    'title'
]

MARKER_VALID_KEYS = [
    'symbol',
    'line',
    'size',
    'color',
    'opacity'
]

MARKER_SAFE_KEYS = [
    'symbol',
    'size'
]

LEGEND_VALID_KEYS = [
    'bgcolor',
    'bordercolor',
    'font',
    'traceorder'
]

LEGEND_SAFE_KEYS = [
    'traceorder'
]

LINE_VALID_KEYS = [
    'dash',
    'color',
    'width',
    'opacity'
]

LINE_SAFE_KEYS = [
    'dash'
]

MARGIN_VALID_KEYS = [
    'l',
    'r',
    'b',
    't',
    'pad'
]

MARGIN_SAFE_KEYS = [
    'l',
    'r',
    'b',
    't',
    'pad'
]

FONT_VALID_KEYS = [
    'color',
    'size',
    'family'
]

FONT_SAFE_KEYS = []

ANNOTATION_VALID_KEYS = [
    'text',
    'bordercolor',
    'borderwidth',
    'borderpad',
    'bgcolor',
    'xref',
    'yref',
    'showarrow',
    'arrowwidth',
    'arrowcolor',
    'arrowhead',
    'arrowsize',
    'tag',
    'font',
    'opacity',
    'align',
    'xanchor',
    'yanchor',
    'ay',
    'ax',
    'y',
    'x'
]

ANNOTATION_SAFE_KEYS = [
    'text',
    'xref',
    'yref',
    'showarrow',
    'align',
    'xanchor',
    'yanchor',
    'ay',
    'ax',
    'y',
    'x'
]

