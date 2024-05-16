import polars as pl
from typing import Any, Dict, Optional
import numpy as np
from vortice.config_global import GhgDataset
from vortice.config_data_fields import GhgNumericField, GhgDiagnosticField
import logging


@pl.api.register_dataframe_namespace("flux")
class FluxDataFrame:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def config(self, metadata: GhgDataset) -> list[pl.DataFrame]:
        self.metadata = metadata
        meta_columns = [self.metadata.time_column] + [
            f.name for f in self.metadata.columns
        ]

        # Check that the column names are unique
        if len(self._df.columns) != len(self._df.columns):
            raise ValueError(
                f"Config columns has duplicated names."
            )
        
        # Check that the time column is of type datetime
        if not isinstance(self._df[self.metadata.time_column].dtype, pl.Datetime):
            raise ValueError(
                f"Time column '{self.metadata.time_column}' must be of type datetime."
            )

        # Adjust and check metadata columns
        for column in meta_columns:
            if column not in self._df.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame.")
        for column in self._df.columns:
            if column not in meta_columns:
                self._df = self._df.drop(column)
                logging.warning(f"Column '{column}' not found in metadata.")

        # Convert the units to default units
        self.convert_to_default_units()

    def wind_direction(self, u: pl.Series, v: pl.Series) -> pl.Series:
        offset = anemometer3d.north_offset - 180.0
        wind_dir = (
            df_hf.select(["TIMESTAMP", "u", "v"])
            .with_columns(
                (180 - pl.arctan2d(pl.col("v"), pl.col("u")) + offset)
                .mod(360)
                .alias("wind_dir")
            )
            .select(["TIMESTAMP", "wind_dir"])
        )




    def convert_to_default_units(self):
        for field in self.metadata.columns:
            if isinstance(field, GhgNumericField):
                self._df = self._df.with_columns(
                    field.convert_units(self._df[field.name]).alias(field.name)
                )
        

    def _set_is_daytime(self):

        if self.metadata.is_day_alg == "eddypro":
            solar_time_delta = self.metadata.lon * 4 + self.metadata.flux_window / 2
            solar_time = self._df["timestamp"].dt.delta(minutes=solar_time_delta)
            self._df["is_daytime"] = solar_time.apply(
                lambda x: self.is_daytime(self.metadata.lat, x)
            )
