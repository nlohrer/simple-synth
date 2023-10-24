const url = "http://localhost:6500";
const head = document.querySelector('#head');
const submit = document.querySelector("#submit");
submit.addEventListener("click", addWAVs)

const wavContainer = document.querySelector("#wav-container");
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
const envelopeContainer = document.querySelector("#envelope-container");
const envelopeGraph = document.querySelector("#envelope-graph")
const graphWidth = envelopeContainer.getAttribute("width");
const graphHeight = envelopeContainer.getAttribute("height");

const envelopeFields = [secondsField, attackField, decayField, releaseField];
envelopeFields.forEach((field) => {
    field.addEventListener("input", () => {
        keepEnvelopeBalance();
        updateEnvelopeGraph();
    });
});
keepEnvelopeBalance();
updateEnvelopeGraph();


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
}

function addWAVToContainer(created_url) {
    const idExpr = /\/\d+\./g;
    const idContext = created_url.match(idExpr)[0];
    const id = idContext.slice(1, -1);

    const audioContainer = document.createElement("div")
    const deleteButton = document.createElement("button")
    const audio = document.createElement("audio");
    const source = document.createElement("source");

    audio.toggleAttribute("controls");
    audioContainer.classList.add("audio-container");
    audioContainer.appendChild(audio);
    audioContainer.appendChild(deleteButton);
    wavContainer.appendChild(audioContainer);

    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => {
        deleteWAV(id);
        audioContainer.remove();
    });

    source.setAttribute("src", created_url);
    source.setAttribute("type", "audio/wav");

    audio.appendChild(source);
}

async function createWAV(frequency, duration, amplitude, waveform, envelope) {
    const body = `{"frequency": ${frequency}, "seconds": ${duration}, "amplitude": ${amplitude}, "waveform": "${waveform}", "envelope": ${envelope}}`;
    const response = await fetch(`${url}/synth`, {
        method: 'POST',
        headers: {
            'content-type': 'application/json'
        },
        body: body
    });

    const created_url = response.headers.get('location');
    return created_url;
}

async function deleteWAV(id) {
    await fetch(`${url}/synth/${id}`, {
        method: 'DELETE'
    });
}

async function getInfo() {
    const response = await fetch(url);
    const response_text = await response.text()
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
}

function updateEnvelopeGraph() {
    const coordinateArray = new Array(5);
    const seconds = secondsField.value;
    const unit = graphWidth / seconds

    const newAttack = Math.round(attackField.value * unit);
    if (newAttack == graphWidth) {
        envelopeGraph.setAttribute("d", `M0,${Math.round(graphHeight)} L${graphWidth},0`);
        return;
    }
    const newDecay = Math.round(decayField.value * unit);
    const newRelease = Math.round(releaseField.value * unit);
    const newSeconds = Math.round(seconds * unit);

    coordinateArray[0] = `M0,${graphHeight}`
    coordinateArray[1] = `L${newAttack},0`;
    coordinateArray[2] = `L${newAttack + newDecay},${Math.round(graphHeight/2)}`;
    coordinateArray[3] = `L${newSeconds - newRelease},${Math.round(graphHeight/2)}`;
    coordinateArray[4] = `L${graphWidth},${graphHeight}`;

    if (newAttack === 0) {
        if (newDecay === 0) {
            coordinateArray[0] = `M0,${Math.round(graphHeight/2)}`
            coordinateArray[1] = `L0,${Math.round(graphHeight/2)}`
        } else {
        coordinateArray[0] = `M0,0`;
        }
    }
    if (newRelease === 0) {
        coordinateArray[4] = `L${graphWidth},${Math.round(graphHeight/2)}`
    }

    const newCoordinateArray = coordinateArray.join(" ");
    envelopeGraph.setAttribute("d", newCoordinateArray);
}