FROM python:3-alpine

WORKDIR /src

COPY . .
#COPY ../synth ./synth
RUN pip install -r ./requirements.txt
RUN mkdir ./static

EXPOSE 6500

CMD ["flask", "--app", "api", "run", "--host", "0.0.0.0", "--port", "6500"]
