# -*- coding: utf-8 -*-

"""Handle Highcharts parameters built from pandas DataFrame with a
Javascript-like object.

Use case:

   from pandas_highcharts.core import serialize
   data = serialize(df, render_to="content", title="My Data", output_type="json")
   # 'data' is a Python dict.
   # Instead of doing:
   data["xAxis"]["type"] = "new_type"
   # You would like to do (with autocompletion in an interactive Python)
   data.xAxis.type = "new_type"
"""

from __future__ import print_function
import copy
import json

import numpy as np
import pandas as pd

from munch import Munch, munchify, unmunchify

from core import serialize


def series_data_filter(data):
    """Replace each 'data' key in the list stored under 'series' by "[...]".

    Use to not store and display the series data when you just want display and
    modify the Highcharts parameters.
    """
    data = copy.deepcopy(data)
    if "series" in data:
        for series in data["series"]:
            series["data"] = "[...]"
    return data

def highcharts_param(data):
    """Return a Javascript-like object with Munch.

    data: dict

    Return the Highcharts parameters as a Javascript-like object.
    """
    return munchify(series_data_filter(data))

def pretty_json(data, indent=2):
    """Pretty print your Highcharts params (into a JSON).
    """
    print(json.dumps(data, indent=indent))

def inject_series_data(data, js, inplace=False):
    """From the 'raw' Highcharts params, re-inject all series data into the
    js.series[:].data.

    data: dict
       Raw data from pandas_highcharts serializer
    js: Javascript-like object
       Where the js.series[:].data had been replaced for readability
    inplace: bool (False)
       Do not copy.

    """
    if inplace:
        result = js
    else:
        result = Munch(copy.deepcopy(js))
    for idx, values in enumerate(data["series"]):
        result.series[idx].data = values
    return result


if __name__ == '__main__':
    ts = pd.date_range("2014/03/15", periods=20, freq="B")
    df = pd.DataFrame({"A": np.sin(np.arange(20)/2.),
                       "Q": 2. + np.cos(np.arange(20)/1.5)},
                      index=ts)
    data = serialize(df, render_to="content", output_type="json")
    js = highcharts_param(data)
    js.series[0].name = "New lineplot name"
    pretty_json(js)
    js2 = inject_series_data(data, js)
