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
setInterval(showSlides, 900000); // 

// timer image only

let slideIndex2 = 0;
const slides2 = document.querySelectorAll(".slideshow-container2 img");

function showSlides2() {
    slides2.forEach((slide) => slide.classList.remove("active"));
    slideIndex2 = (slideIndex2 + 1) % slides2.length;
    slides2[slideIndex2].classList.add("active");
}
function slidesReset() {
    slides2.forEach((slide) => slide.classList.remove("active"));
    slideIndex2 = 0;
    slides2[0].classList.add("active");
}
/*   
* Stop Watch Script for use after the timer hits 0
* This should ideally only occur for 10 minutes now
*/ 
var startTime;
var stopwatchInterval;
let slideTriggered = false;
function startStopwatch() { 
    stopTimer(); 
    if (!stopwatchInterval) {
        startTime = new Date().getTime();
        slideTriggered = false; 
        stopwatchInterval = setInterval(updateStopwatch, 1000);
    }
}

function updateStopwatch() {
    var currentTime = new Date().getTime();
    var elapsedTime = currentTime - startTime; 
    
    var totalSecondsElapsed = Math.floor(elapsedTime / 1000);
    var minutes = Math.floor(totalSecondsElapsed / 60);
    var seconds = totalSecondsElapsed % 60;

    document.getElementById("timer-display").innerHTML = "-" + pad(minutes) + ":" + pad(seconds);

    // Trigger image change only ONCE at the 10-minute mark (600,000 ms)
    if (elapsedTime >= 600000 && !slideTriggered) {
        showSlides2();
        slideTriggered = true; 
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
let totalSeconds = 1800; // Default timer = 1800 // 5 in DEV
let isRunning = false;

function updateDisplay() {
    const minutes = Math.floor(totalSeconds / 60);
    const displaySeconds = totalSeconds % 60;
    document.getElementById("timer-display").textContent = pad(minutes) + ":" + pad(displaySeconds);
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
    totalSeconds = 1800; // 1800 default timer
}

function adjustTimer() {
    stopThem();
    resetThem();
    const newTime = prompt("Enter countdown time in minutes:");
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        totalSeconds = parseInt(newTime) * 60; // Convert minutes to seconds
        updateDisplay();
    }
}

function setAndStart(mins) {
    stopThem();
    totalSeconds = mins * 60;
    updateDisplay();
    startTimer();
}

function minutesFive() { setAndStart(8); } // 5 + 3 seating/review

function minutesThirty() { setAndStart(33); } // 30 + 3 seating/review

function minutesFifty() { setAndStart(53); } // 50 + 3 seating/review

function stopThem() {
    stopTimer();
    stopStopwatch();
}

function resetThem() {
    resetTimer();
    resetStopwatch();
}

// Timer Visibility Toggle
function toggleTimerVisibility() {
    const timerContainer = document.getElementById("timer-container");
    timerContainer.style.display = (timerContainer.style.display === "none") ? "flex" : "none";
}

function goHome() {
    // If the countdown is running OR the stopwatch is active
    if (isRunning || stopwatchInterval) {
        const leave = confirm("A timer is currently active. Are you sure you want to go back to the Home Page? This will reset the clock!");
        
        if (leave) {
            window.location.href = 'index.html';
        }
    } else {
        // If nothing is running, just go home without asking
        window.location.href = 'index.html';
    }
}