import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import altair
import seaborn as sns

from . import utils


def render(chart):
    """Render an Altair chart as a matplotlib figure

    Parameters
    ----------
    chart : altair.Chart
        a Chart, LayeredChart, or FacetedChart to render

    Returns
    -------
    fig : matplotlib.Figure
        the rendered Figure

    Raises
    ------
    NotImplementedError :
        Many portions of the Vega-Lite schema are not yet supported, and this
        routine raises a NotImplementedError when it encounters them.
    """
    # dispatch on chart type
    if isinstance(chart, altair.Chart):
        return _render_chart(chart)
    elif isinstance(chart, altair.LayeredChart):
        return _render_layeredchart(chart)
    elif isinstance(chart, altair.FacetedChart):
        return _render_facetedchart(chart)
    elif isinstance(chart, dict):
        return render(altair.Chart.from_dict(chart))
    elif isinstance(chart, string):
        return render(altair.Chart.from_json(chart))


def _defined_traits(obj):
    if not obj:
        return []
    else:
        return [t for t in obj.trait_names() if getattr(obj, t)]


def _render_chart(chart):
    if chart.mark == 'line':
        return _render_line_chart(chart)
    elif chart.mark == 'text' and 'color' in chart.to_dict()['encoding']:
        return _render_heatmap(chart)
    else:
        raise NotImplementedError("mark = {0}".format(chart.mark))


def _render_heatmap(chart):
    data = utils.chart_data(chart)
    encoding = chart.to_dict()['encoding']
    column, row, color = [encoding[key]['field']
                         for key in ['column', 'row', 'color']]
    if encoding['text']['field'] not in {None, ' ', ''}:
        kwargs = {'annot': True}
    else:
        kwargs = {'annot': False}

    data = data.pivot_table(columns=column, index=row, values=color)
    return sns.heatmap(data, **kwargs)


def _render_line_chart(chart):
    data = utils.chart_data(chart)
    encodings = _defined_traits(chart.encoding)

    if chart.encoding.color:
        groups = data.groupby(chart.encoding.color.field)
        legend = True
    else:
        groups = [None, data]
        legend = False

    fig, ax = plt.subplots()

    for color, group in groups:
        ax.plot(group[chart.encoding.x.field],
                group[chart.encoding.y.field],
                label=str(color))

    if legend:
        ax.legend(title=chart.encoding.color.field)

    return fig


def _render_layeredchart(chart):
    raise NotImplementedError("Faceted Chart")


def _render_facetedchart(chart):
    raise NotImplementedError("Layered Chart")
