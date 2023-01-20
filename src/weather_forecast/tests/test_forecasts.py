import sys

sys.path.append(
    "/home/guus/python/projects/assignment/weather_forecast/src/weather_forecast"
)
import unittest
from datetime import datetime, timedelta, timezone
from unittest import TestCase

import pandas
from forecasts import Forecasts


class TestForecasts(unittest.TestCase):
    def setUp(self):
        now = datetime(2021, 1, 27, 1, 30, 50, tzinfo=timezone.utc)
        self.then = datetime(2021, 1, 28, 2, tzinfo=timezone.utc)

        self.forecasts = Forecasts("src/weather_forecast/tests/test_weather.csv")

    def test_get_latest_forecast(self):

        value = self.forecasts.get_latest_forecast(
            "2021-01-28 02:00:00+00", 13000, "temperature"
        )

        self.assertEqual(value, 20.47)

    def test_get_belief_horizon_in_sec(self):
        belief_horizon_in_sec = self.forecasts.get_belief_horizon_in_sec(
            datetime(2021, 1, 27, 1, 30, 0, tzinfo=timezone.utc),
            datetime(2021, 1, 28, 2, tzinfo=timezone.utc),
        )

        self.assertEqual(belief_horizon_in_sec, 88200)

    def test_transform_then_to_datasource_format(self):
        then_in_datasource_format = self.forecasts.transform_then_to_datasource_format(
            datetime(2021, 1, 28, 2, tzinfo=timezone.utc)
        )

        self.assertEqual(then_in_datasource_format, "2021-01-28 02:00:00+00")
