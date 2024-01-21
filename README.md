# CO2 tracker app

## Purpose

This app is a script intended to be run daily to gather the previous day French energetic mix
CO2 emission data.

## Design decisions

### Architecture

The CO2 tracker script is designed with a modular and extensible architecture to facilitate future
enhancements and adaptability. The main components include a records fetcher, responsible for
obtaining CO2 data from external APIs, and a records writer, managing the output of CO2 records
either to files or the console. The use of dependency injection allows for dynamic configuration
of these components, making it easy to swap out implementations or extend functionality without
modifying the core logic. The script employs a command-line interface, making it easy to configure
the source of data and output preferences.

### Usage of UTC times

The script uses UTC as the standard timezone. This choice is aimed at streamlining operations and
minimizing potential issues related to time zone conversions. The responsibility for displaying
localized datetime information should be delegated to the frontend.

### Requirements

- [click](https://click.palletsprojects.com/en/8.1.x/): a CLI builder tool
- [httpx](https://www.python-httpx.org/): a performant alternative to requests supporting both
  synchronous and asynchronous requests
- [pydantic](https://docs.pydantic.dev/latest/): a fast and extensible data validation library

## Extending the script functionalities

### Adding a fetcher

It is easy to add a new fetcher (e.g. fetching data from a different API):

- write a fetcher class implementing to the RecordsFetcherInterface
- add it as a new strategy in the `records_fetcher_builder` function in `main.py`

### Adding a writer

It is easy to add a new writer (e.g. writing the records to a database):

- write a fetcher class implementing to the RecordsWriterInterface
- add it as a new strategy in the `records_writer_builder` function in `main.py`

## How to run

### Running manually

Use the `--help` command to show the different parameters

```shell
❯ python3.11 -m venv venv && source venv/bin/activate
❯ python main.py --help
Usage: main.py [OPTIONS]

Options:
  --fetcher [ecoco2mix]    API from which to fetch C02 data
  --writer [file|console]  Writer to which records are outputed
  --folder TEXT            Folder to which files are stored (if writer=file)
  --prefix TEXT            Filename prefix (if writer=file)
  --help                   Show this message and exit.


❯  python main.py --writer=console  # Outputs the records to the console
❯  python main.py --writer=file  --folder="~"  # Outputs the records to a file in the HOME directory
```

### Running with Docker

The following commands will run the script and output the CO2 records in a file in an `/output`
folder in the current working directory.

```shell
❯ mkdir output
❯ docker build -t co2-tracker-docker .
❯ docker run -v "$(pwd)"/output:/app/output co2-tracker-docker
```

## Potential next steps

- [ ] Fetch data from another API for redundancy
- [ ] Allow for a more frequent run frequency (e.g. fetching data every hour instead of every day)
- [ ] Implement new writer classes (e.g. write to a DB) so the data is more easily usable