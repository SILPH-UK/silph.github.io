/*  
* Slideshow Script to govern how frequently the images rotate on the home "Index" / "Dev" screen
*/
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
setInterval(showSlides, 5000); // Change slide every 5 seconds - DEV Only

// timer image only

let slideIndex2 = 0;
const slides2 = document.querySelectorAll(".slideshow-container2 img");

function showSlides2() {
    slides2.forEach((slide, index) => {
        slide.classList.remove("active");
        if (index === slideIndex2) {
            slide.classList.add("active");
        }
    });
    slideIndex2 = (slideIndex2 + 1) % slides2.length;
}
function slidesReset() {
    slides2.forEach((slide, index) => {
        slide.classList.remove("active");
        if (index === slideIndex2) {
            slide.classList.add("active");
        }
    });
    slideIndex2 = 0;
}
/*   
* Stop Watch Script for use after the timer hits 0
* This should ideally only occur for 10 minutes now
*/ 
var startTime;
var stopwatchInterval;
function startStopwatch() { 
    updateDisplay();
    stopTimer(); // Stop the timer when it reaches zero
    if (!stopwatchInterval) {
        startTime = new Date().getTime();
        stopwatchInterval = setInterval(updateStopwatch, 1000);
    }
}

function updateStopwatch() {
    var currentTime = new Date().getTime(); // get current time in milliseconds
    var elapsedTime = currentTime - startTime; // calculate elapsed time in milliseconds
    var seconds = Math.floor(elapsedTime / 1000) % 60; // calculate seconds
    var minutes = Math.floor(elapsedTime / 1000 / 60) % 60; // calculate minutes
    //var hours = Math.floor(elapsedTime / 1000 / 60 / 60); // calculate hours
    var displayTime = "-" + pad(minutes) + ":" + pad(seconds); // format display time
    if (elapsedTime < 5000) { // 600000 for 10 minutes
        document.getElementById("timer-display").innerHTML = displayTime; // update the display
    } else if (elapsedTime > 5000 && elapsedTime < 7000) { // 600000 for 10 minutes
        document.getElementById("timer-display").innerHTML = displayTime; // update the display
        showSlides2();
        document.getElementById("timer-display").innerHTML = displayTime; // update the display
    } else {
        document.getElementById("timer-display").innerHTML = displayTime; // update the display
    }
}

function pad(number) {
    // add a leading zero if the number is less than 10
    return (number < 10 ? "0" : "") + number;
}

function stopStopwatch() {
    clearInterval(stopwatchInterval); // stop the interval
    elapsedPausedTime = new Date().getTime() - startTime; // calculate elapsed paused time
    stopwatchInterval = null; // reset the interval variable
}

function resetStopwatch() {
    stopStopwatch(); // stop the interval
    elapsedPausedTime = 0; // reset the elapsed paused time variable
    document.getElementById("timer-display").innerHTML = "00:00"; // reset the display
    slidesReset(); // In theory this should just rotate back to the base image
}

/*
* // Countdown Timer Script
*/
let timer;
let totalSeconds = 5; // Default timer = 1800 // 5 in DEV
let isRunning = false;

function updateDisplay() {
    const minutes = Math.floor(totalSeconds / 60);
    const displaySeconds = totalSeconds % 60;
    if (totalSeconds > 0) {
        document.getElementById("timer-display").textContent =
            (minutes < 10 ? "0" : "") + minutes + ":" +
            (displaySeconds < 10 ? "0" : "") + displaySeconds;   
    }
}

/* 
* Button scripts
*/

function startTimer() {
    if (!isRunning && totalSeconds > 0) { // Start only if timer is set and not running
        isRunning = true;
        timer = setInterval(() => {
            if (totalSeconds > 0) {
                totalSeconds--;
                updateDisplay();
            } else {
                updateDisplay();
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

function stopThem() {
    stopTimer()
    stopStopwatch()
}

function resetThem() {
    resetTimer()
    resetStopwatch()
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
