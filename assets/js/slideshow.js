/**
 * CONFIGURATION & CONSTANTS
 */
const SETTINGS = {
    DEFAULT_MINUTES: 30,
    BUFFER_MINUTES: 3,
    STOPWATCH_TRIGGER_MS: 900000, // 15 mins: Transitions timer-specific image
    BG_ROTATION_MS: 60000        // 1 mins: How often background images rotate
};

/**
 * UI & DOM ELEMENTS
 */
const UI = {
    backgroundSlides: document.querySelectorAll(".slideshow-container img"),
    timerSlides: document.querySelectorAll(".slideshow-container2 img"),
    display: document.getElementById("timer-display"),
    container: document.getElementById("timer-container"),

    // Shared logic to set a specific slide active
    setActiveSlide(slides, index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === index);
        });
    },

    pad: (num) => num.toString().padStart(2, '0')
};

/**
 * INDEPENDENT BACKGROUND SLIDESHOW
 * Runs automatically, independent of timer/stopwatch
 */
let bgIndex = 0;
const backgroundAutoCycle = setInterval(() => {
    bgIndex = (bgIndex + 1) % UI.backgroundSlides.length;
    UI.setActiveSlide(UI.backgroundSlides, bgIndex);
}, SETTINGS.BG_ROTATION_MS);

/**
 * TIMER & STOPWATCH STATE
 */
const Clock = {
    timerInterval: null,
    stopwatchInterval: null,
    totalSeconds: SETTINGS.DEFAULT_MINUTES * 60,
    startTime: null,
    isRunning: false,
    stopwatchTriggered: false,

    // --- Countdown Methods ---
    startCountdown() {
        if (this.isRunning) return;
        this.isRunning = true;
        
        this.timerInterval = setInterval(() => {
            if (this.totalSeconds > 0) {
                this.totalSeconds--;
                this.refreshDisplay();
            } else {
                this.stopCountdown();
                this.startStopwatch();
            }
        }, 1000);
    },

    stopCountdown() {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
        this.isRunning = false;
    },

    // --- Stopwatch Methods (Tied to container2) ---
    startStopwatch() {
        if (this.stopwatchInterval) return;
        this.startTime = Date.now();
        this.stopwatchTriggered = false;

        this.stopwatchInterval = setInterval(() => {
            const elapsed = Date.now() - this.startTime;
            const totalSecs = Math.floor(elapsed / 1000);
            
            // Format for display: -MM:SS
            const m = Math.floor(totalSecs / 60);
            const s = totalSecs % 60;
            UI.display.textContent = `-${UI.pad(m)}:${UI.pad(s)}`;

            // Trigger secondary image change ONLY at the 10-minute mark
            if (elapsed >= SETTINGS.STOPWATCH_TRIGGER_MS && !this.stopwatchTriggered) {
                UI.setActiveSlide(UI.timerSlides, 1); 
                this.stopwatchTriggered = true;
            }
        }, 1000);
    },

    refreshDisplay() {
        const m = Math.floor(this.totalSeconds / 60);
        const s = this.totalSeconds % 60;
        UI.display.textContent = `${UI.pad(m)}:${UI.pad(s)}`;
    },

    resetAll() {
        this.stopCountdown();
        clearInterval(this.stopwatchInterval);
        this.stopwatchInterval = null;
        this.totalSeconds = SETTINGS.DEFAULT_MINUTES * 60;
        this.stopwatchTriggered = false;

        // Reset only the timer-specific image to the first one
        UI.setActiveSlide(UI.timerSlides, 0);
        this.refreshDisplay();
    }
};

/**
 * BUTTON / INTERFACE ACTIONS
 */
function setAndStart(mins) {
    Clock.resetAll();
    Clock.totalSeconds = (mins + SETTINGS.BUFFER_MINUTES) * 60;
    Clock.refreshDisplay();
    Clock.startCountdown();
}

// User-facing button triggers
const minutesFive = () => setAndStart(5);
const minutesThirty = () => setAndStart(30);
const minutesFifty = () => setAndStart(50);

function adjustTimer() {
    const newTime = prompt("Enter countdown time in minutes:");
    if (newTime !== null && !isNaN(newTime) && newTime >= 0) {
        Clock.resetAll();
        Clock.totalSeconds = parseInt(newTime) * 60;
        Clock.refreshDisplay();
    }
}

function stopThem() {
    Clock.stopCountdown();
    clearInterval(Clock.stopwatchInterval);
    Clock.stopwatchInterval = null;
}

function goHome() {
    if (Clock.isRunning || Clock.stopwatchInterval) {
        if (confirm("A timer is active. Reset and go home?")) {
            window.location.href = 'index.html';
        }
    } else {
        window.location.href = 'index.html';
    }
}

function toggleTimerVisibility() {
    const isHidden = UI.container.style.display === "none";
    UI.container.style.display = isHidden ? "flex" : "none";
}