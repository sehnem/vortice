from dataclasses import dataclass, field
from typing import Optional, List
from abc import ABC
import pendulum
import polars as pl


@dataclass
class SiteConfig:
    """
    Dataclass for GHG metadata.
    """
    name: str
    lat: float
    lon: float
    alt: float
    canopy_height: float
    roughness_length: Optional[float] = field(default=None)

    def __post_init__(self):
        if self.roughness_length is None:
            self.roughness_length = 0.15 * self.canopy_height


@dataclass
class InstrumentConfig(ABC):
    name: str
    manufacturer: Optional[str] = None
    local_id: Optional[str] = None
    serial: Optional[str] = None
    model: Optional[str] = None
    sw_version: Optional[str] = None


@dataclass
class GhgDataField:
    name: str
    variable: str
    unit: Optional[str] = None
    instrument: Optional[InstrumentConfig] = None


@dataclass
class GhgDataset:
    name: str
    site: SiteConfig
    columns: List[GhgDataField]
    time_column: str
    tz: str = "UTC"
    period: Optional[int] = None
    freq: Optional[int] = None


    def __post_init__(self):
        # Check that only one of 'period' or 'freq' is set
        if self.period is not None and self.freq is not None:
            raise ValueError("Only one of 'period' or 'freq' can be set.")
        elif self.period is None and self.freq is None:
            raise ValueError("Either 'period' or 'freq' must be set.")
        elif self.period:
            self.freq = 1 / self.period
        elif self.freq:
            self.period = 1 / self.freq

    def set_pendulum_tz(self, timezone: str):
        self.tz = pendulum.timezone(timezone).name
