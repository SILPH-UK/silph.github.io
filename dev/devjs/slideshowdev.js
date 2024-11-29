// Slideshow Script
let slideIndex = 0;
const slides = document.querySelectorAll(".slideshow-container img");

function showSlides() {
    slides.forEach((slide, index) => {
        slide.classList.remove("active");
        if (index === slideIndex) {
            slide.classList.add("active");
        }
    });
    slideIndex = (slideIndex + 1) % slides.length;
}
setInterval(showSlides, 5000); // Change slide every 5 seconds - DEV ONLY

// Stop Watch Script

var startTime;
var stopwatchInterval;
function startStopwatch() { // for use after the timer hits 0
    stopTimer(); // Stop the timer when it reaches zero
    if (!stopwatchInterval) {
        startTime = new Date().getTime();
        stopwatchInterval = setInterval(updateStopwatch, 1000)
    }
}

function updateStopwatch() {
    var currentTime = new Date().getTime(); // get current time in milliseconds
    var elapsedTime = currentTime - startTime; // calculate elapsed time in milliseconds
    var seconds = Math.floor(elapsedTime / 1000) % 60; // calculate seconds
    var minutes = Math.floor(elapsedTime / 1000 / 60) % 60; // calculate minutes
    //var hours = Math.floor(elapsedTime / 1000 / 60 / 60); // calculate hours
    var displayTime = "-" + pad(minutes) + ":" + pad(seconds); // format display time
    document.getElementById("stopwatch-display").innerHTML = displayTime; // update the display
}

function pad(number) {
    // add a leading zero if the number is less than 10
    return (number < 10 ? "0" : "") + number;
}

// Countdown Timer Script
let timer;
let totalSeconds = 1800; // Default timer
let isRunning = false;

function updateDisplay() {
    const minutes = Math.floor(totalSeconds / 60);
    const displaySeconds = totalSeconds % 60;
    document.getElementById("timer-display").textContent =
        (minutes < 10 ? "0" : "") + minutes + ":" +
        (displaySeconds < 10 ? "0" : "") + displaySeconds;
}

function startTimer() {
    if (!isRunning && totalSeconds > 0) { // Start only if timer is set and not running
        isRunning = true;
        timer = setInterval(() => {
            if (totalSeconds > 0) {
                totalSeconds--;
                updateDisplay();
            } else {
                //stopTimer(); // Stop the timer when it reaches zero
                //alert("Time's up!");
                startStopwatch();
            }
        }, 1000);
    }
}

function stopTimer() {
    isRunning = false;
    clearInterval(timer);
}

function resetTimer() {
    stopTimer();
    totalSeconds = 0;
    updateDisplay();
}

function adjustTimer() {
    const newTime = prompt("Enter countdown time in minutes:");
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        totalSeconds = parseInt(newTime) * 60; // Convert minutes to seconds
        updateDisplay();
    }
}

function minutesFive() {
    stopTimer();
    const newTime = 300 / 60;
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        totalSeconds = parseInt(newTime) * 60; // Convert minutes to seconds
        updateDisplay();
        startTimer();
    }
}

function minutesThirty() {
    stopTimer();
    const newTime = 1800 / 60; //let totalSeconds = 1800
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        totalSeconds = parseInt(newTime) * 60; // Convert minutes to seconds
        updateDisplay();
        startTimer();
    }
}

function minutesFifty() {
    stopTimer();
    const newTime = 3000 / 60;
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        totalSeconds = parseInt(newTime) * 60; // Convert minutes to seconds
        updateDisplay();
        startTimer();
    }
}

// Timer Visibility Toggle
function toggleTimerVisibility() {
    const timerContainer = document.getElementById("timer-container");
    if (timerContainer.style.display === "none") {
        timerContainer.style.display = "flex"; // Show timer
    } else {
        timerContainer.style.display = "none"; // Hide timer
    }
}
