from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import List

class BarType(str, Enum):
    TICKS = "TICKS"
    DAY = "DAY"
    MINUTE = "MINUTE"

class Instrument(BaseModel):
    name: str
    expiration_date: date
    tick_currency_value: float

class TimeFrame(BaseModel):
    name: str
    bars_type: BarType
    value: int

class BarData(BaseModel):
    open: float
    low: float
    high: float
    close: float
    volume: int
    ema9_value: float
    ema21_value: float
    bar_datetime: datetime

class DataSeries(BaseModel):
    instrument: Instrument
    timeframe: TimeFrame
    list_of_bars: List[BarData]
    init_date: date
    end_date: date