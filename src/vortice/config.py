import polars as pl
from typing import Any, Dict, Optional
import re
import pendulum
from dataclasses import dataclass, field
import numpy as np
import numpy as np
from datetime import datetime
from enum import Enum
from vortice.config_def import GhgDataset
import logging

# biomet data
# Ambient temperature, pressure and relative humidity - available in eddycovariance but less precise
# Data of global radiation and long-wave incoming radiation can be used in the
# multiple regression” version of the off-season uptake correction (Burba et al.2008)
# Data of photosynthetically active radiation (PAR, also called PPFD, photosynthetic photon flux density) can be used to assess day and night-time radiation loading on the surface of the instrument, to apply the appropriate coefficients and modeling of the instrument surface temperature in the off-season uptake correction.






@pl.api.register_dataframe_namespace("flux")
class FluxDataFrame:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def config(self, metadata: GhgDataset) -> list[pl.DataFrame]:
        self.metadata = metadata
        meta_columns = [self.metadata.time_column] + [f.name for f in self.metadata.columns]

        for column in meta_columns:
            if column not in self._df.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame.")
        for column in self._df.columns:
            if column not in meta_columns:
                self._df = self._df.drop(column)
                logging.warning(f"Column '{column}' not found in metadata.")
        
        if not isinstance(self._df[self.metadata.time_column].dtype, pl.Datetime):
            raise ValueError(f"Time column '{self.metadata.time_column}' must be of type datetime.")
        
        

    def _set_is_daytime(self):

        if self.metadata.is_day_alg == "eddypro":
            solar_time_delta = self.metadata.lon * 4 + self.metadata.flux_window / 2
            solar_time = self._df["timestamp"].dt.delta(minutes=solar_time_delta)
            self._df["is_daytime"] = solar_time.apply(
                lambda x: self.is_daytime(self.metadata.lat, x)
            )
