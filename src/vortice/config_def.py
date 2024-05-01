from dataclasses import dataclass
from typing import Optional
from abc import ABC
import pendulum


class GhgSite:
    """
    Dataclass for GHG metadata
    """
    def __init__(
        self,
        name: str,
        lat: float,
        lon: float,
        alt: float,
        canopy_height: float,
        roughness_length: Optional[float] = None,
        flux_window: int = 30
    ) -> None:
        self.name = name
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.canopy_height = canopy_height

        if self.roughness_length is None:
            self.roughness_length = 0.15 * self.canopy_height
        else:
            self.roughness_length = roughness_length
        self.flux_window = flux_window



class InstrumentConfig(ABC):
    
    def __init__(
            self,
            name: str
        ) -> None:
        self.name = name


class GhgDataField:

    def __init__(
        self,
        name: str,
        variable: str,
        unit: str,
        instrument: Optional[InstrumentConfig] = None
    ) -> None:
        self.name = name
        self.variable = variable
        self.unit = unit
        self.instrument = instrument


class GhgDataset(ABC):

    def __init__(
        self,
        name: str,
        columns: list[GhgDataField],
        tz: str = "UTC",
        freq: int = 10
    ) -> None:
        self.name = name
        self.columns = columns
        self.tz = tz
        self.freq = freq

    @property
    def pendulum_tz(self, timezone: str):
        self.tz = pendulum.timezone(timezone)






@dataclass
class Anemometer3DConfig(InstrumentConfig):
    manufacturer: str
    model: str
    height: float
    sw_version: Optional[str] = None
    serial: Optional[str] = None
    local_id: Optional[str] = None
    wref: Optional[str] = None
    north_offset: Optional[float] = 0.0
    northward_separation: Optional[float] = 0.0
    eastward_separation: Optional[float] = 0.0
    vertical_separation: Optional[float] = 0.0
    vpath_length: Optional[float] = 1.0
    hpath_length: Optional[float] = 1.0
    tau: Optional[float] = 0.1

@dataclass
class GasAnalyzer(InstrumentConfig):
    manufacturer: str
    model: str
    sw_version: Optional[str] = None
    serial: Optional[str] = None
    local_id: Optional[str] = None
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