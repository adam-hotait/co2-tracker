from datetime import datetime, date
from typing import Iterator

import httpx
import pydantic

from app import models
from app.services.records_fetcher.records_fetcher_interface import (
    RecordsFetcherInterface,
)


class _EcoCO2APIRecord(pydantic.BaseModel):
    date: str
    hour: int
    co2: float


class EcoCO2Mix(RecordsFetcherInterface):
    def __init__(self):
        self.api_url = (
            "https://odre.opendatasoft.com/"
            "api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records"
        )

    def fetch_co2_records(self, previous_day: date) -> models.CO2Records:
        # Builds the query params in UTC format (see README.md for explanation on usage of UTC)
        params = {
            "select": "date, avg(taux_co2) as co2",
            "where": f"date='{previous_day.strftime('%Y-%m-%d')}'",
            "group_by": "date,hour(date_heure) as hour",
            "limit": "24",
            "timezone": "UTC",
        }

        # Queries the API
        resp = httpx.get(
            self.api_url,
            params=params,
        )

        # Handles API errors
        if resp.status_code != 200:
            raise RuntimeError(f"EcoCO2Mix API returned a {resp.status_code} response")

        # Serializes the records and returns
        # The sorting is done at this step because there is an issue with the order_by clause
        # of the API (it returns hours as int, but it sorts them as strings)
        return models.CO2Records(
            root=sorted(
                [
                    self._parse_api_record(record)
                    for record in self._parse_results(resp.json()["results"])
                ],
                key=lambda el: el.datetime,
            )
        )

    @staticmethod
    def _parse_results(results: dict[str, dict]) -> Iterator[_EcoCO2APIRecord]:
        yield from pydantic.TypeAdapter(list[_EcoCO2APIRecord]).validate_python(results)

    @staticmethod
    def _parse_api_record(record: _EcoCO2APIRecord) -> models.CO2Record:
        return models.CO2Record(
            co2_rate=record.co2,
            datetime=datetime.fromisoformat(f"{record.date}T{record.hour:02d}:00:00Z"),
        )
