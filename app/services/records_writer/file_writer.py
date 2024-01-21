import os
from datetime import date

from app import models
from app.services.records_writer.records_writer_interface import RecordsWriterInterface


class FileWriter(RecordsWriterInterface):
    def __init__(self, folder: str, prefix: str = "co2_records"):
        self.folder = folder
        if folder.startswith("~"):
            self.folder = os.path.expanduser(folder)
        self.prefix = prefix

    def write_co2_records(
        self, previous_day: date, co2_records: models.CO2Records
    ) -> None:
        filename = os.path.join(
            self.folder, f"{self.prefix}_{previous_day.strftime('%Y-%m-%d')}.json"
        )
        with open(filename, "w", encoding="utf-8") as writer:
            writer.write(co2_records.model_dump_json())
