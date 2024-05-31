var button = document.getElementById('startButton');
var trialNumber = document.getElementById('trialNumber');
const blockSize = document.getElementById('blockSize');
const algorithm = document.getElementById('algorithm');
const sensor = document.getElementById('sensor');
const sensorSelection = document.getElementById('sensorSelection');
const enableFieldsCheckbox = document.getElementById('enableFieldsCheckbox');
const nextStimElement = document.getElementById('nextStimulation');
const currentStimElement = document.getElementById('currentStimulation');
const patientRTElement = document.getElementById('patientRT');

function updateHTMLContent(data) {
    // Update HTML content with received data
    nextStimElement.value = "qqq";
}

function enableSensorFields() {
    sensor.disabled = false;
}

function disableSensorFields() {
    sensor.disabled = true;
}

function enableTrialFields() {
    trialNumber.disabled = false;
    blockSize.disabled = false;
    algorithm.disabled = false;
}

function disableTrialFields() {
    trialNumber.disabled = true;
    blockSize.disabled = true;
    algorithm.disabled = true;
}

function sendDataToMainProcess() {
    const data = {};
    if (sensorSelection.checked) {
        data.CommandType = "Sensor selection";
        data.sensor = sensor.value;
    } else {
        if (!trialNumber.disabled) {
            data.CommandType = "Task Configuration";
            data.trialNumber = parseInt(trialNumber.value, 10);
            data.blockSize = parseInt(blockSize.value, 10);
            data.algorithm = algorithm.value;
        }
    }
    // Create a new object with CommandType and Data fields
    var jsonData = {
        CommandType: data.CommandType,
        Data: data
    };
    window.electronAPI.setTitle(JSON.stringify(jsonData));
}

function toggledata() {
    if (sensorSelection.checked) {
        enableSensorFields();
        disableTrialFields();
    } else {
        disableSensorFields();
        enableTrialFields();
    }
}

button.addEventListener('click', sendDataToMainProcess);
sensorSelection.addEventListener('change', toggledata);
enableFieldsCheckbox.addEventListener('change', function() {
    if (enableFieldsCheckbox.checked) {
        enableTrialFields();
    } else {
        disableTrialFields();
    }
});


// In your renderer process JavaScript file (renderer.js)

// Listen for the 'dataFromPubSubServer' event from the main process
// This assumes you've exposed ipcRenderer through contextBridge
  window.electronAPI.SendMsgToUITitle((value) => {
    console.log("not sure")
    nextStimElement.innerText = value.toString()
  })