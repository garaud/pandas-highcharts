# -*- coding: utf-8 -*-

from .core import serialize, json_encode
import datetime
import pandas
from unittest import TestCase

df = pandas.DataFrame([
    {"a": 1, "b": 2, "c": 3, "t": datetime.date(2015, 1, 1)},
    {"a": 2, "b": 4, "c": 6, "t": datetime.date(2015, 1, 2)}
])


class CoreTest(TestCase):
    def test_type(self):
        self.assertEqual(type(serialize(df, render_to="chart")), str)
        obj = serialize(df, render_to="chart", output_type="json")
        self.assertEqual(type(obj), dict)
        obj = serialize(df, render_to="chart", output_type="json", zoom="xy")
        self.assertTrue("chart" in obj)
        self.assertEqual(type(obj["chart"]), dict)
        self.assertTrue("zoomType" in obj["chart"])
        self.assertRaises(ValueError, serialize, df, **{"render_to": "chart", "zoom": "z"})
        obj = serialize(df, render_to="chart", output_type="json", kind="bar")
        self.assertTrue("chart" in obj)
        self.assertEqual(type(obj["chart"]), dict)
        self.assertEqual(obj["chart"].get("type"), "column")
        self.assertRaises(ValueError, serialize, df, **{"render_to": "chart", "kind": "z"})
        obj = serialize(df, render_to="chart", output_type="json", secondary_y="a")
        self.assertTrue(obj.get("yAxis", [])[1].get('opposite'))
        obj = serialize(df, render_to="chart", output_type="json", rot=45, loglog=True)
        self.assertEqual(obj.get('xAxis', {}).get('labels'), {'rotation': 45})
        self.assertEqual(obj.get('yAxis', [])[0].get('labels'), {'rotation': 45})
        self.assertEqual(obj.get('xAxis', {}).get('type'), 'logarithmic')
        obj = serialize(df, render_to="chart", output_type="json", x="t")
        self.assertEqual(obj.get('xAxis', {}).get('type'), 'datetime')
        obj = serialize(df, render_to="chart", output_type="json", x="t", style={"a": ":"})
        for series in obj.get("series"):
            if series["name"] == "a":
                self.assertEqual(series.get("dashStyle"), "Dot")
        self.assertRaises(ValueError, serialize, df, **{"render_to": "chart", "style": {"a": "u"}})
        obj = serialize(df, render_to="chart", output_type="json", kind="area", stacked=True)
        self.assertEqual(obj.get("series")[0].get("stacking"), "normal")

        obj = serialize(df, render_to="chart", output_type="json", grid=True)
        self.assertEqual(obj.get('xAxis', {}).get('gridLineDashStyle'), 'Dot')
        self.assertEqual(obj.get('xAxis', {}).get('gridLineWidth'), 1)
        self.assertEqual(obj.get('yAxis', [])[0].get('gridLineDashStyle'), 'Dot')
        self.assertEqual(obj.get('yAxis', [])[0].get('gridLineWidth'), 1)

        obj = serialize(df, render_to="chart", output_type="json", xlim=(0, 1), ylim=(0, 1))
        self.assertEqual(obj.get('xAxis', {}).get('min'), 0)
        self.assertEqual(obj.get('xAxis', {}).get('max'), 1)
        self.assertEqual(obj.get('yAxis', [])[0].get('min'), 0)
        self.assertEqual(obj.get('yAxis', [])[0].get('max'), 1)

        obj = serialize(df, render_to="chart", output_type="json", fontsize=12)
        self.assertEqual(obj.get('xAxis', {}).get('labels', {}).get('style', {}).get('fontSize'), 12)
        self.assertEqual(obj.get('yAxis', [])[0].get('labels', {}).get('style', {}).get('fontSize'), 12)

    def test_jsonencoder(self):
        self.assertEqual(json_encode(datetime.date(1970, 1, 1)), "0")
        self.assertEqual(json_encode(datetime.date(2015, 1, 1)), "1420070400000")
        self.assertEqual(json_encode(datetime.datetime(2015, 1, 1)), "1420070400000")
        self.assertEqual(json_encode(pandas.tslib.Timestamp(1420070400000000000)), "1420070400000")
