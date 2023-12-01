# simple-synth
Simple synth using Python to create basic sine, square, sawtooth or square waves. examples.py in the synth directory includes some examples for creating such waves and for basic additive synthesis.

To create .wav files for sine waves via command line, you can use "python synth/sine.py [frequency] [length] [filename]"

For example, "python synth/sine.py 440 5 a.wav" creates a 5 second long sine wave pitched at A440.

## Docker-compose
Simply run `docker compose --env-file .env.dev up -d` in the root directory and go to `http://localhost:10000` in a browser of your choice. To stop and remove the containers, run `docker compose --env-file .env.dev down`.

## Web app

To run the web app locally on Linux, first install all dependencies and run the API:

```bash
git clone https://github.com/nlohrer/simple-synth.git
cd simple-synth/flask
mkdir static
cp ../web/* static
python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
flask --app api run --port 6500
```

Afterwards, open `http://localhost:6500/static/index.html` in a browser of your choice.

To run the app on Windows, you can run the same commands in powershell, only replacing the steps to create and activate the virtual environment:

```powershell
git clone https://github.com/nlohrer/simple-synth.git; `
Set-Location simple-synth/flask; `
New-Item static -ItemType Directory; `
Copy-Item ..\web\* static; `
python -m venv .venv; `
.\.venv\Scripts\activate; `
pip install -r requirements.txt; `
flask --app api run --port 6500
```

All created wav files are stored in the directory `static`. Some bugs you encounter while using the app might be solved by deleting its contents or by rerunning the API.
