from datetime import date

from app import models
from app.services.records_writer.records_writer_interface import RecordsWriterInterface


class ConsoleWriter(RecordsWriterInterface):
    """
    Streams each record to stdout
    """

    def write_co2_records(
        self, previous_day: date, co2_records: models.CO2Records
    ) -> None:
        for record in co2_records.root:
            print(record.model_dump_json())
