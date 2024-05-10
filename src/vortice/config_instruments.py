from dataclasses import dataclass, field
from typing import Optional, List
from abc import ABC
import pendulum

from vortice.config_global import InstrumentConfig


@dataclass
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

@dataclass
class GasAnalyzerConfig(InstrumentConfig):
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