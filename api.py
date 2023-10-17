from flask import Flask
from flask import request
import os
from urllib.parse import urlparse
import synth

app = Flask(__name__)

@app.route("/")
def information():
    return "To create a .wav file, send a POST request to /synth/<id>"

# Example usage:
# $ curl -iX "POST" "localhost:6500/synth/1" -H "content-type: application/json" -d {"frequency": 440, "seconds": 2}
# The response body includes the path to the created .wav file
@app.post("/synth/<id>")
def hello_world(id):
    current_working_directory = os.getcwd();
    file_path = f"/static/{id}.wav"
    local_path = f"{current_working_directory}{file_path}"

    freq, sec, = request.json['frequency'], request.json['seconds'];

    synth.sin_to_file(freq = freq, sec = sec, fname = local_path)
    url = urlparse(request.base_url)
    hostname = url.hostname
    port = url.port
    return f"{hostname}:{port}{file_path}"
