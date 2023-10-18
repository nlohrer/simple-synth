from flask import Flask
from flask import request
from flask import Response
import os
from urllib.parse import urlparse
import synth

app = Flask(__name__)

@app.route("/")
def information():
    response =  Response("To create a .wav file, send a POST request to /synth/<id>")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Example usage:
# $ curl -iX "POST" "localhost:6500/synth/1" -H "content-type: application/json" -d '{"frequency": 440, "seconds": 2}'
# The response body includes the path to the created .wav file
@app.route("/synth/<id>", methods=['OPTIONS', 'POST'])
def createWAV(id):

    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response
    
    current_working_directory = os.getcwd();
    file_path = f"/static/{id}.wav"
    local_path = f"{current_working_directory}{file_path}"

    freq, sec, = request.json['frequency'], request.json['seconds'];
    amplitude = request.json.get('amplitude')
    amp = 0.1
    
    if (amplitude):
        amp = set_amplitude(amplitude, freq)

    synth.sin_to_file(freq = freq, sec = sec, amp = amp, fname = local_path)

    url = urlparse(request.base_url)
    hostname = url.hostname
    port = url.port
    response = Response(f"{hostname}:{port}{file_path}", 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    
    return response

def set_amplitude(amplitude, freq):
    # these are somewhat arbitrarily defined limits for amplitude; the upper limit for amplitude increases with frequency to prevent loss of hearing
    if freq <= 300:
        upper_limit = 1
    elif freq <= 500:
        upper_limit = 0.7
    elif freq <= 700:
        upper_limit = 0.5
    elif freq <= 1000:
        upper_limit = 0.25
    elif freq <= 8000:
        upper_limit = 0.1
    else:
        upper_limit = 0.05
    amp = amplitude if amplitude <= upper_limit else upper_limit  # Preventing the creation of extremely loud sounds
    return amp