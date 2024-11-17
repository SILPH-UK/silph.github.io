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
setInterval(showSlides, 60000); // Change slide every 60 seconds

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
                stopTimer(); // Stop the timer when it reaches zero
                alert("Time's up!");
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
    const newTime = prompt("Enter countdown time in minutes:", totalSeconds / 60);
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        totalSeconds = parseInt(newTime) * 60; // Convert minutes to seconds
        updateDisplay();
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
