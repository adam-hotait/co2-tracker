import abc
from datetime import date

from app import models


class RecordsFetcherInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_co2_records(self, previous_day: date) -> models.CO2Records:
        """
        Fetches the CO2 records for a given day and returns grouped by hour, in chronological order
        """
