"""
Here the calculations for the forcasts and the tomorrow value will be calculated.
"""

from datetime import datetime, timedelta, timezone

import pandas


class Forecasts:

    weather_dataframe = pandas.read_csv(
        "/home/guus/python/projects/assignment/weather_forecast/src/weather_forecast/weather.csv"
    )

    def get_forecast(self, now, then):
        belief_horizon_in_sec = self.get_belief_horizon_in_sec(now, then)
        then_in_datasource_format = self.transform_then_to_datasource_format(then)
        forecast = {}

        for sensor_type in ["temperature", "irradiance", "wind speed"]:
            forecast[sensor_type] = self.get_latest_forecast(
                then_in_datasource_format, belief_horizon_in_sec, sensor_type
            )

        return forecast

    def get_latest_forecast(self, then, belief_horizon_in_sec, sensor_type):
        forecasts_dataframe = self.weather_dataframe[
            (self.weather_dataframe["event_start"] == then)
            & (self.weather_dataframe["sensor"] == sensor_type)
            & (self.weather_dataframe["belief_horizon_in_sec"] >= belief_horizon_in_sec)
        ]

        if forecasts_dataframe.empty:
            return "No forecasts for this date range"
        event_value = forecasts_dataframe.loc[
            forecasts_dataframe["belief_horizon_in_sec"].idxmin()
        ]["event_value"]

        return event_value

    def get_belief_horizon_in_sec(self, now, then):
        belief_horizon_in_sec = (then - now).total_seconds()

        return belief_horizon_in_sec

    def transform_then_to_datasource_format(self, then):
        then = datetime(
            then.year, then.month, then.day, then.hour, 0, tzinfo=timezone.utc
        ).isoformat()
        then_in_datasource_format = then[:-3].replace("T", " ")

        return then_in_datasource_format

    def get_tommorow(self, now):
        tommorow = now + timedelta(days=1)
        # get the next day
        # get the latest forecast for each time
        # get the max forecast for the 3 booleans

        pass

    def get_tomorrow_datetime_in_datasource_format(self, now):
        tommorow = now + timedelta(days=1)
        tommorow_start = datetime(
            tommorow.year, tommorow.month, tommorow.day, 0, 0, tzinfo=timezone.utc
        ).isoformat()
        tommorow_end = datetime(
            tommorow.year, tommorow.month, tommorow.day, 24, 0, tzinfo=timezone.utc
        ).isoformat()

        tommorow_start_in_datasource_format = tommorow_start[:-3].replace("T", " ")
        tommorow_end_in_datasource_format = tommorow_end[:-3].replace("T", " ")

        return tommorow_start_in_datasource_format, tommorow_end_in_datasource_format
