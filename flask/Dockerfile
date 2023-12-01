FROM python:3-alpine

WORKDIR /src/flask

COPY ./flask .
COPY ./synth ../synth
RUN mkdir ./static
RUN pip install -r ./requirements.txt
RUN pip install gunicorn

EXPOSE 6500

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:6500", "api:app"]
