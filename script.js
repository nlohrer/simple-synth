url = "http://localhost:6500";
const head = document.querySelector('#head');
const submit = document.querySelector("#submit");
var id = 1;
submit.addEventListener("click", addWAVs)

const frequencyField = document.querySelector("#frequency");
const secondsField = document.querySelector("#sec");
const ampField = document.querySelector("#amp");
const waveformField = document.querySelector("#waveform");
const attackField = document.querySelector("#attack");
const decayField = document.querySelector("#decay");
const releaseField = document.querySelector("#release");
const attackLabel = document.querySelector("#attack-label");
const decayLabel = document.querySelector("#decay-label");
const releaseLabel = document.querySelector("#release-label");

envelopeFields = [secondsField, attackField, decayField, releaseField];
keepEnvelopeBalance();
envelopeFields.forEach((field) => {
    field.addEventListener("input", keepEnvelopeBalance);
});


async function addWAVs() {
    const frequency = frequencyField.value.trim();
    const seconds = secondsField.value.trim();
    const amplitude = ampField.value.trim();
    const waveform = waveformField.value;
    const attack = attackField.value;
    const decay = decayField.value;
    const release = releaseField.value;
    const envelope = `{"attack": ${attack}, "decay": ${decay}, "release": ${release}}`

    const wavURL = await createWAV(frequency, seconds, amplitude, waveform, envelope);
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

async function createWAV(frequency, duration, amplitude, waveform, envelope) {
    body = `{"frequency": ${frequency}, "seconds": ${duration}, "amplitude": ${amplitude}, "waveform": "${waveform}", "envelope": ${envelope}}`;
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

async function getInfo() {
    response = await fetch(url);
    response_text = await response.text()
    console.log(response_text);
}

function keepEnvelopeBalance() {
    const seconds = secondsField.value.trim();
    const attack = attackField.value;
    const decay = decayField.value;
    const release = releaseField.value;

    const attackRemainder = seconds - decay - release;
    const decayRemainder = seconds - attack - release;
    const releaseRemainder = seconds - attack - decay;

    attackField.max = attackRemainder > 0 ? attackRemainder : 0;
    decayField.max = decayRemainder ? decayRemainder : 0;
    releaseField.max = releaseRemainder ? releaseRemainder : 0;

    attackLabel.textContent = `Attack: ${parseFloat(attack).toFixed(2)}`;
    decayLabel.textContent = `Decay: ${parseFloat(decay).toFixed(2)}`;
    releaseLabel.textContent = `Release: ${parseFloat(release).toFixed(2)}`;

    console.log("---------------")
    console.log("attack max:" + attackField.max);
    console.log("decay max:" + decayField.max);
    console.log("release max:" + releaseField.max);
}