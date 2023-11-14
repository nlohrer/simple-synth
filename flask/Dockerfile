FROM python:3-alpine

WORKDIR /src/flask

COPY ./flask .
COPY ./synth ../synth
RUN mkdir ./static
RUN pip install -r ./requirements.txt

EXPOSE 6500

CMD ["flask", "--app", "api", "run", "--host", "0.0.0.0", "--port", "6500"]
