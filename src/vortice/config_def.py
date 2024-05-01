from dataclasses import dataclass, field
from typing import Optional
from abc import ABC, List
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
    dataset: Optional[pl.DataFrame]
    tz: str = "UTC"
    period: Optional[int] = None
    freq: Optional[int] = None


    def __post_init__(self):

        # Check that only one of 'period' or 'freq' is set
        if self.period is not None and self.freq is not None:
            raise ValueError("Only one of 'period' or 'freq' can be set.")
        elif self.period:
            self.freq = 1 / self.period
        elif self.freq:
            self.period = 1 / self.freq

    def set_pendulum_tz(self, timezone: str):
        self.tz = pendulum.timezone(timezone).name
    




class Anemometer3DConfig(InstrumentConfig):
    height: Optional[float] = 3.0
    wref: Optional[str] = None
    north_offset: Optional[float] = 0.0
    northward_separation: Optional[float] = 0.0
    eastward_separation: Optional[float] = 0.0
    vertical_separation: Optional[float] = 0.0
    vpath_length: Optional[float] = 1.0
    hpath_length: Optional[float] = 1.0
    tau: Optional[float] = 0.1


class GasAnalyzer(InstrumentConfig):
    tube_length: Optional[float] = 0.0
    tube_diameter: Optional[float] = 0.0
    tube_flowrate: Optional[float] = 0.0
    northward_separation: Optional[float] = 0.0
    eastward_separation: Optional[float] = 0.0
    vertical_separation: Optional[float] = 0.0
    vpath_length: Optional[float] = 1.0
    hpath_length: Optional[float] = 1.0
    tau: Optional[float] = 0.1
    kw: Optional[float] = 0.15
    ko: Optional[float] = 0.0085