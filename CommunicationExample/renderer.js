

var holdertext = document.getElementById('holdertext');
var button = document.getElementById('myButton');
var randomNumberElement1 = document.getElementById('randomNumber1');
var randomNumberElement2 = document.getElementById('randomNumber2');
var randomNumberElement3 = document.getElementById('randomNumber3');
var responsevar = document.getElementById('responseElement');
var Reactiontime = document.getElementById('Reactiontime');
var sequenceNumber = document.getElementById('sequenceNumber');
var Reactiontimehistory = document.getElementById('Reactiontimehistory');
var reactionTimes = [];
var reactionaccuracy = [];
var seqNumber = 0;
var startTime = 0;
var endTime = 0;
var responseTime = endTime - startTime;

// Function to plot the reaction time history
function plotReactionTimeHistory(data, plotelement, labelname) {
    // Get the canvas element
    var ctx = document.getElementById(plotelement).getContext('2d');

    // Create a new chart
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i + 1), // Trial labels
            datasets: [{
                label: labelname,
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Trial'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: labelname
                    }
                }
            }
        }
    });
}

function generateRandomNumber() {
    var randomNumber = Math.floor(Math.random() * 3) + 1;
    return randomNumber;
}

function seqUpdate() {
    seqNumber = seqNumber + 1;
    sequenceNumber.textContent = seqNumber;
}

function startsession() {
    randomNumberElement1.textContent = generateRandomNumber();
    randomNumberElement2.textContent = generateRandomNumber();
    randomNumberElement3.textContent = generateRandomNumber();
    startTime = performance.now();
    seqUpdate();
}


// Function to handle key press event
function handleKeyPress(event) {
    // Check if the pressed key is the number "1"
    if (reactionTimes.length < 21) {
        if (event.key === "1" || event.key === "2" || event.key === "3") {
            // Update the label with the key pressed
            endTime = performance.now();
            if (randomNumberElement2.textContent === event.key) {
                responsevar.textContent = "correct";
                reactionaccuracy.push(1);
            }
            else {
                responsevar.textContent = "incorrect";
                reactionaccuracy.push(0);
            }
            responseTime = endTime - startTime;
            try {
                window.electronAPI.setTitle(responseTime.toFixed(2));
            } catch (error) {
                
            }
            Reactiontime.textContent = "Response Time: " + responseTime.toFixed(2) + " milliseconds";
            reactionTimes.push(responseTime);
            startsession();
            startTime = performance.now();
        }
    }
    else {
        holdertext.textContent = "session ended";
        plotReactionTimeHistory(reactionTimes, 'reactionTimeChart', 'Reaction time (ms)');
        plotReactionTimeHistory(reactionaccuracy, 'reactionTimeaccuracy', 'Accuracy');
        Reactiontimehistory.textContent = "Reaction Time History: " + reactionTimes.map(time => time.toFixed(2)).join(", ");
    }
}


// Add a click event listener to the button
button.addEventListener('click', startsession);

// Add a keydown event listener to the document
document.addEventListener('keydown', handleKeyPress);

