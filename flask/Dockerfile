FROM python:3-alpine

WORKDIR /src/flask

COPY ./flask .
COPY requirements.txt .
COPY ./synth ../synth
RUN mkdir ./static
RUN pip install -r ./requirements.txt
RUN pip install gunicorn

EXPOSE $FLASK_PORT

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:6500", "api:app"]