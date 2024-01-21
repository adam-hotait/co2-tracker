FROM python:3.11

# Install dependencies
COPY ./requirements /requirements
RUN pip install -r /requirements/requirements.txt

COPY main.py /app/main.py
COPY ./app /app/app

RUN mkdir app/output

ENTRYPOINT [ "python", "app/main.py", "--writer=file", "--folder=/app/output" ]
