from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from vortice.config_global import InstrumentConfig
from typing import Optional, Dict
from abc import ABC, abstractmethod
import polars as pl

from collections import namedtuple

UnitConversion = namedtuple("UnitConversion", ["factor", "offset"], defaults=[1.0, 0])


@dataclass
class GhgDataField(ABC):
    name: str
    instrument: InstrumentConfig


@dataclass
class GhgNumericField(GhgDataField):
    unit: str
    default_unit: str = None
    variable: str = None
    measurement_type: str = "sample"

    measurement_types_mapping = {"sample": pl.mean, "max": pl.max, "min": pl.min}

    def __post_init__(self):
        # get the aggregation operation for polars
        if self.measurement_type not in ["sample", "max", "min"]:
            raise ValueError(f"Invalid measurement type '{self.measurement_type}'")
        self.agg_op = self.measurement_types_mapping[self.measurement_type]

    @property
    @abstractmethod
    def conversion_mapping(self) -> Dict[str, UnitConversion]:
        raise NotImplementedError("conversion_mapping must be implemented in subclass")

    def conversion_factor(self, unit: str) -> UnitConversion:
        try:
            current_fact = self.conversion_mapping[self.unit]
            conv_fact = self.conversion_mapping[unit]
        except KeyError:
            valid_units = list(self.conversion_mapping.keys())
            raise ValueError(
                f"Invalid unit '{self.unit}', valid units are {valid_units}"
            )
        target_offset = current_fact.offset - conv_fact.offset
        target_factor = current_fact.factor / conv_fact.factor
        return UnitConversion(factor=target_factor, offset=target_offset)

    def convert_units(
        self, col_data: pl.Series, unit: Optional[str] = None
    ) -> pl.Series:
        """Convert all columns to their default units."""
        unit = self.default_unit if unit is None else unit
        if unit == self.unit:
            return col_data

        factor = self.conversion_factor(unit)
        self.unit = unit
        return col_data * factor.factor + factor.offset

    def validation(self):
        raise NotImplementedError("Validation method must be implemented in subclass")


@dataclass
class GhgDiagnosticField(GhgDataField):

    def validation(self):
        return True


@dataclass
class TemperatureField(GhgNumericField):
    variable: str = "temperature"
    default_unit: str = "k"
    conversion_mapping = {
        "k": UnitConversion(),
        "c": UnitConversion(factor=1, offset=273.15),
        "f": UnitConversion(factor=5 / 9, offset=459.67),
    }


@dataclass
class PressureField(GhgNumericField):
    variable: str = "pressure"
    default_unit: str = "Pa"
    conversion_mapping = {
        "Pa": UnitConversion(),
        "hPa": UnitConversion(factor=1e-2),
        "kPa": UnitConversion(factor=1e-3),
        "bar": UnitConversion(factor=1e-5),
        "atm": UnitConversion(factor=9.86923e-6),
    }


@dataclass
class RadiationField(GhgNumericField):
    variable: str = "radiation"
    default_unit: str = "W/m2"
    conversion_mapping = {
        "W/m2": UnitConversion(),
        "W/cm2": UnitConversion(factor=1e4),
        "kW/m2": UnitConversion(factor=1e-3),
        "kW/cm2": UnitConversion(factor=1e1),
    }


@dataclass
class WindSpeedField(GhgNumericField):
    variable: str = "wind_speed"
    default_unit: str = "m/s"
    conversion_mapping = {
        "m/s": UnitConversion(),
        "km/h": UnitConversion(factor=3.6),
        "mph": UnitConversion(factor=2.23694),
        "knots": UnitConversion(factor=1.94384),
    }


@dataclass
class Wind3dUField(WindSpeedField):
    variable: str = "wind_speed_u"


@dataclass
class Wind3dVField(WindSpeedField):
    variable: str = "wind_speed_v"


@dataclass
class Wind3dWField(WindSpeedField):
    variable: str = "wind_speed_w"


@dataclass
class GasField(GhgNumericField):
    variable: str = "gas_name"


@dataclass
class H2OField(GhgNumericField):
    variable: str = "h20"


@dataclass
class CH4Field(GhgNumericField):
    variable: str = "co2"


@dataclass
class CH4Field(GhgNumericField):
    variable: str = "ch4"
