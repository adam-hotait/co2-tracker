from datetime import datetime, timedelta

import click

from app.services.logger import logger
from app.services.records_fetcher.eco_co2_fetcher import EcoCO2Mix
from app.services.records_fetcher.records_fetcher_interface import (
    RecordsFetcherInterface,
)
from app.services.records_writer.file_writer import FileWriter
from app.services.records_writer.records_writer_interface import RecordsWriterInterface
from app.services.records_writer.console_writer import ConsoleWriter


@click.command()
@click.option(
    "--fetcher",
    default="ecoco2mix",
    help="API from which to fetch C02 data",
    type=click.Choice(["ecoco2mix"], case_sensitive=False),
)
@click.option(
    "--writer",
    default="file",
    help="Writer to which records are outputed",
    type=click.Choice(["file", "console"], case_sensitive=False),
)
@click.option(
    "--folder", default="~", help="Folder to which files are stored (if writer=file)"
)
@click.option(
    "--prefix", default="co2_records", help="Filename prefix (if writer=file)"
)
def main(fetcher, writer: str, folder: str, prefix: str) -> None:
    logger.info("Started CO2 tracker script")
    Launcher(
        records_fetcher_builder(fetcher), records_writer_builder(writer, folder, prefix)
    ).run()
    logger.info("Finished running CO2 tracker script with no errors")


def records_fetcher_builder(fetcher) -> RecordsFetcherInterface:
    if fetcher == "ecoco2mix":
        return EcoCO2Mix()
    raise NotImplementedError


def records_writer_builder(writer, folder, prefix) -> RecordsWriterInterface:
    if writer == "file":
        return FileWriter(folder=folder, prefix=prefix)
    if writer == "console":
        return ConsoleWriter()
    raise NotImplementedError


class Launcher:
    def __init__(
        self,
        records_fetcher: RecordsFetcherInterface,
        records_writer: RecordsWriterInterface,
    ):
        self.records_fetcher = records_fetcher
        self.records_writer = records_writer

    def run(self):
        yesterday = (datetime.now() - timedelta(1)).date()
        co2_records = self.records_fetcher.fetch_co2_records(yesterday)
        self.records_writer.write_co2_records(yesterday, co2_records)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
