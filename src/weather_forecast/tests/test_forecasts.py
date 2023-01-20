import unittest
from datetime import datetime, timedelta, timezone
from unittest import TestCase

import pandas
from forecasts import Forecasts


class TestForecasts(unittest.TestCase):
    def setUp(self):
        now = datetime(2021, 1, 27, 1, 30, 50, tzinfo=timezone.utc)
        self.then = datetime(2021, 1, 28, 2, tzinfo=timezone.utc)

        weather_dataframe = pandas.read_csv(
            "/home/guus/python/projects/assignment/weather_forecast/src/weather_forecast/tests/test_weather.csv"
        )

        self.Forecasts = Forecasts()
        self.Forecasts.weather_dataframe = weather_dataframe

    def test_get_latest_forecast(self):

        value = self.Forecasts.get_latest_forecast(self.then, 13000, "temperature")

        self.assertEqual(value, 20.47)
