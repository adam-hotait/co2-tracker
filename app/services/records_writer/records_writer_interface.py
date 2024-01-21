import abc
from datetime import date

from app import models


class RecordsWriterInterface(abc.ABC):
    @abc.abstractmethod
    def write_co2_records(
        self, previous_day: date, co2_records: models.CO2Records
    ) -> None:
        """
        Writes the CO2 records to a specific output
        """
