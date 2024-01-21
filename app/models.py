from datetime import datetime

import pydantic


class CO2Record(pydantic.BaseModel):
    datetime: datetime
    co2_rate: float


class CO2Records(pydantic.RootModel):
    root: list[CO2Record]
