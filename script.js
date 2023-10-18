url = "http://localhost:6500";
const head = document.querySelector('#head');
const submit = document.querySelector("#submit");
var id = 1;

submit.addEventListener("click", addWAVs)

async function addWAVs() {
    const frequencyField = document.querySelector("#frequency");
    const secondsField = document.querySelector("#sec");
    const ampField = document.querySelector("#amp");
    const waveformField = document.querySelector("#waveform");
    const frequency = frequencyField.value.trim();
    const seconds = secondsField.value.trim();
    const amplitude = ampField.value.trim();
    const waveform = waveformField.value;

    const wavURL = await createWAV(frequency, seconds, amplitude, waveform);
    addWAVToContainer(wavURL);
    console.log(wavURL);
}

function addWAVToContainer(url) {
    const container = document.querySelector("#wav-container");
    const full_url = `http://${url}`;

    const audio = document.createElement("audio");
    audio.toggleAttribute("controls");
    container.appendChild(audio);

    const source = document.createElement("source");
    source.setAttribute("src", full_url);
    source.setAttribute("type", "audio/wav");
    audio.appendChild(source);
}

async function getInfo() {
    response = await fetch(url);
    response_text = await response.text()
    console.log(response_text);
}

async function createWAV(frequency, duration, amplitude, waveform) {
    body = `{"frequency": ${frequency}, "seconds": ${duration}, "amplitude": ${amplitude}, "waveform": "${waveform}"}`;
    response = await fetch(`${url}/synth/${id++}`, {
        method: 'POST',
        headers: {
            'content-type': 'application/json'
        },
        body: body
    });

    response_text = await response.text();
    return response_text;
}