import polars as pl
from typing import Any, Dict, Optional
import re
import pendulum
from dataclasses import dataclass, field
import numpy as np
import numpy as np
from datetime import datetime
from enum import Enum


# biomet data
# Ambient temperature, pressure and relative humidity - available in eddycovariance but less precise
# Data of global radiation and long-wave incoming radiation can be used in the
# multiple regression” version of the off-season uptake correction (Burba et al.2008)
# Data of photosynthetically active radiation (PAR, also called PPFD, photosynthetic photon flux density) can be used to assess day and night-time radiation loading on the surface of the instrument, to apply the appropriate coefficients and modeling of the instrument surface temperature in the off-season uptake correction.






@pl.api.register_dataframe_namespace("flux")
class FluxDataFrame:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    def config(self, metadata: GHGMetadata) -> list[pl.DataFrame]:
        self.metadata = GHGMetadata.update(metadata)

    def _set_is_daytime(self):

        if self.metadata.is_day_alg == "eddypro":
            solar_time_delta = self.metadata.lon * 4 + self.metadata.flux_window / 2
            solar_time = self._df["timestamp"].dt.delta(minutes=solar_time_delta)
            self._df["is_daytime"] = solar_time.apply(
                lambda x: self.is_daytime(self.metadata.lat, x)
            )
