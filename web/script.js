const url = "..";
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
const attackLabel = document.querySelector("#attack-value");
const decayLabel = document.querySelector("#decay-value");
const releaseLabel = document.querySelector("#release-value");
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

/**
 * Reads wav parameters from the form, then sends them to the API and creates an audio-container using the returned url.
 */
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

    // hashing current time and adding it to URL to prevent browsers from using cached versions of deleted files
    const stamped_URL = wavURL + '?' + Date.now().toString(36);     

    addWAVToContainer(stamped_URL);
}

/**
 * Uses the url of a wav file to add a an audio-container to the website, which contains an audio element, a download button and a delete button for the wav file.
 * @param created_url The url for the wav file, which was read from the location header of the API response to the POST request.
 */
function addWAVToContainer(created_url) {
    const idExpr = /\/\d+\./g;
    const idContext = created_url.match(idExpr)[0];
    const id = idContext.slice(1, -1);

    /*
    Structure of the audio container:
    <div class="audio-container">
        <audio controls="">
            <source src={created_url} type="audio/wav">
        </audio>
        <form action={created_url} method="get">
            <button>Download</button>
        </form>
        <button>Delete</button>
    </div>
    */
    const audioContainer = document.createElement("div")
    const deleteButton = document.createElement("button")
    const downloadForm = document.createElement("form");
    const downloadButton = document.createElement("button")
    const audio = document.createElement("audio");
    const source = document.createElement("source");

    audio.toggleAttribute("controls");
    audioContainer.classList.add("audio-container");
    audioContainer.appendChild(audio);
    audioContainer.appendChild(downloadForm);
    downloadForm.appendChild(downloadButton);
    audioContainer.appendChild(deleteButton);
    wavContainer.appendChild(audioContainer);

    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => {
        deleteWAV(id);
        audioContainer.remove();
    });

    downloadForm.action = created_url;
    downloadForm.method = "get";
    downloadButton.textContent = "Download";

    source.setAttribute("src", created_url);
    source.setAttribute("type", "audio/wav");

    audio.appendChild(source);
}

/**
 * Uses the given parameters to send a POST request to the API and returns the url to the newly created wav file
 * @param frequency The frequency of the wav file.
 * @param duration The duration of the wav file in seconds.
 * @param amplitude The amplitude of the wav file, which corresponds to its volume.
 * @param waveform The waveform of the wav file.
 * @param envelope The envelope, which is a JSON object containing values for attack, release and decay (in seconds). Sustain is automatically calculated as sustain = duration - attack - release - decay.
 * @returns The url read from the location header of the response.
 */
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

/**
 * Sends a DELETE request to the API to delete the wav file with the given id
 * @param id The id of the wav file to be deleted.
 */
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

/**
 * Keeps the range inputs for the envelope balanced.
 * 
 * We make use of the invariant duration >= attack + decay + release, leading to inequalities of the form attack <= duration - decay - release. These inequalities then lead to statements of the form max(attack) = duration - decay - release, which we then use to set the max value for the envelope value ranges.
 */
function keepEnvelopeBalance() {
    const seconds = secondsField.value.trim();
    const attack = attackField.value;
    const decay = decayField.value;
    const release = releaseField.value;

    const attackRemainder = seconds - decay - release;
    const decayRemainder = seconds - attack - release;
    const releaseRemainder = seconds - attack - decay;

    attackField.max = attackRemainder;
    decayField.max = decayRemainder;
    releaseField.max = releaseRemainder;

    // ensuring that the value labels never change in width
    attackLabel.textContent = `${parseFloat(attack).toFixed(2)}`;
    decayLabel.textContent = `${parseFloat(decay).toFixed(2)}`;
    releaseLabel.textContent = `${parseFloat(release).toFixed(2)}`;
}

/**
 * Renders the svg graph for the envelope options.
 */
function updateEnvelopeGraph() {
    const coordinateArray = new Array(5);
    const seconds = secondsField.value;
    const unit = graphWidth / seconds

    const attackCoordinates = Math.round(attackField.value * unit);
    if (attackCoordinates == graphWidth) {
        envelopeGraph.setAttribute("d", `M0,${Math.round(graphHeight)} L${graphWidth},0`);
        return;
    }
    const decayCoordinates = Math.round(decayField.value * unit);
    const releaseCoordinates = Math.round(releaseField.value * unit);
    const secondsCoordinates = Math.round(seconds * unit);

    // Using an attack/decay/sustain/release envelope leads to five different points we need to specify for the graph
    coordinateArray[0] = `M0,${graphHeight}`
    coordinateArray[1] = `L${attackCoordinates},0`;
    coordinateArray[2] = `L${attackCoordinates + decayCoordinates},${Math.round(graphHeight/2)}`;
    coordinateArray[3] = `L${secondsCoordinates - releaseCoordinates},${Math.round(graphHeight/2)}`;
    coordinateArray[4] = `L${graphWidth},${graphHeight}`;

    // Some combinations of extreme values mean that some lines should not be rendered
    if (attackCoordinates === 0) {
        if (decayCoordinates === 0) {
            coordinateArray[0] = `M0,${Math.round(graphHeight/2)}`
            coordinateArray[1] = `L0,${Math.round(graphHeight/2)}`
        } else {
        coordinateArray[0] = `M0,0`;
        }
    }
    if (releaseCoordinates === 0) {
        coordinateArray[4] = `L${graphWidth},${Math.round(graphHeight/2)}`
    }

    const newCoordinateArray = coordinateArray.join(" ");
    envelopeGraph.setAttribute("d", newCoordinateArray);
}
