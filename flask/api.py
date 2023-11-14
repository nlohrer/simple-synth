from flask import Flask
from flask import request
from flask import Response
from urllib.parse import urlparse
import os
from sys import path
path.insert(1, '../synth')
import synth


app = Flask(__name__)

used_indices = set()
def get_index():
    global used_indices
    i = 1
    while True:
        if i in used_indices:
            i += 1
            continue
        used_indices.add(i)
        return i

@app.route("/")
def information():
    response =  Response("To create a .wav file, send a POST request to /synth")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/synth/<id_str>", methods=['OPTIONS', 'DELETE'])
def deleteWAV(id_str):
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.add_cors_headers()
        return response

    global used_indices
    id = int(id_str)
    if id not in used_indices:
        response = Response("Error: file with this id does not exist", 404)
        response.add_cors_headers()
        return response
    
    os.remove(f"./static/{id}.wav")
    used_indices.remove(id)
    response = Response(status = 204)
    response.add_cors_headers()
    return response

# Example usage:
# $ curl -iX "POST" "localhost:6500/synth/1" -H "content-type: application/json" -d '{"frequency": 440, "seconds": 2}'
# The response body includes the path to the created .wav file
@app.route("/synth", methods=['OPTIONS', 'POST'])
def createWAV():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.add_cors_headers()
        return response
    
    current_working_directory = os.getcwd()
    id = get_index()
    url_file_path = f"/static/{id}.wav"
    local_path = f"{current_working_directory}{url_file_path}"

    freq, sec, amplitude, waveform, envelope = get_params_from_body(request.json)
    amp, env = correct_parameters(amplitude, envelope, freq, waveform)

    file_function = get_file_function(waveform)
    file_function(freq = freq, sec = sec, amp = amp, fname = local_path, envelope = env)

    response_url = get_response_url(request, url_file_path)
    response = Response(status = 201)
    response.headers['Location'] = response_url
    response.add_cors_headers()
    
    return response

def get_params_from_body(body):
    freq = body['frequency']
    sec = body['seconds']
    amplitude = body.get('amplitude')
    waveform = body.setdefault('waveform', 'sine')
    envelope = body.setdefault('envelope', 'None')
    return freq, sec, amplitude, waveform, envelope

def correct_parameters(amplitude, envelope, freq, waveform):
    amp = 0.1
    if (amplitude):
        amp = set_amplitude(amplitude, freq, waveform)
    if envelope is not None and envelope != "None":
        env = envelope.values()
    else:
        env = None
    return amp, env

def set_amplitude(amplitude, freq, waveform):
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
    # Preventing the creation of extremely loud sounds
    amp = amplitude if amplitude <= upper_limit else upper_limit
    # Sawtooth waves and square waves tend to be louder than others
    if waveform in ('sawtooth', 'square'):
        amp *= 0.8
    return amp

def get_file_function(waveform):
    if waveform == 'sine':
        return synth.sin_to_file
    elif waveform == 'triangular':
        return synth.tri_to_file
    elif waveform == 'sawtooth':
        return synth.saw_to_file
    else:
        return synth.square_to_file

def get_response_url(request, url_file_path):
    url = urlparse(request.base_url)
    protocol = url.scheme
    hostname = url.hostname
    port = url.port
    response_url = f"{protocol}://{hostname}:{port}{url_file_path}"
    return response_url

def add_cors_headers(self):
    self.headers['Access-Control-Allow-Origin'] = '*'
    self.headers['Access-Control-Allow-Methods'] = '*'
    self.headers['Access-Control-Allow-Headers'] = '*'
    self.headers['Access-Control-Expose-Headers'] = 'Location'
Response.add_cors_headers = add_cors_headers