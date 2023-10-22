# simple-synth
Simple synth using Python to create basic sine, square, sawtooth or square waves. examples.py includes some examples for creating such waves and for basic additive synthesis.

To create .wav files for sine waves via command line, you can use "python sine.py [frequency] [length] [filename]"

For example, "python sine.py 440 5 a.wav" creates a 5 second long sine wave pitched at A440.

## Web app

To locally run the web app on Linux, first install all dependencies and run the API:

```bash
git clone https://github.com/nlohrer/simple-synth.git
cd simple-synth
mkdir static
python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
flask --app api run --port 6500
```

Afterwards, open index.html in a browser of your choice.

To run the app on Windows, you can run the same commands in powershell, only replacing the steps to create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

All created wav files are stored in the directory `static`. Some bugs you encounter while using the app might be solved by deleting its contents or by rerunning the API.
