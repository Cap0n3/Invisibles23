// Define content to play
var trackURL = "http://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg";
// Create audio tag element
var currPodcast = document.createElement("audio");
// Load track
document.onload = loadSound(trackURL);
// Timer to update timers
updateTimer = setInterval(seekUpdate, 1000);
// Vars
var isPlaying = false;
// DOM selectors
var playpause_btn = document.querySelector(".playpause-track");
var seek_slider = document.querySelector(".seek_slider");
var curr_time = document.querySelector(".current-time");
var total_duration = document.querySelector(".total-duration");

// === Functions === //
function loadSound(_trackURL) {
    currPodcast.src = _trackURL;
}

function playPodcast() {
    isPlaying = true;
    currPodcast.play();
    playpause_btn.innerHTML =
        '<i class="bi bi-pause-circle" style="font-size: 3em;"></i>';
}

function pausePodcast() {
    isPlaying = false;
    currPodcast.pause();
    playpause_btn.innerHTML =
        '<i class="bi bi-play-circle" style="font-size: 3em;"></i>';
}

function seekUpdate() {
    let seekPosition = 0;
    if (!isNaN(currPodcast.duration)) {
        seekPosition = currPodcast.currentTime * (100 / currPodcast.duration);
        seek_slider.value = seekPosition;

        // Calculate the time left and the total duration
        let currentMinutes = Math.floor(currPodcast.currentTime / 60);
        let currentSeconds = Math.floor(currPodcast.currentTime - currentMinutes * 60);
        let durationMinutes = Math.floor(currPodcast.duration / 60);
        let durationSeconds = Math.floor(currPodcast.duration - durationMinutes * 60);

        // Add a zero to the single digit time values
        if (currentSeconds < 10) {
            currentSeconds = "0" + currentSeconds;
        }
        if (durationSeconds < 10) {
            durationSeconds = "0" + durationSeconds;
        }
        if (currentMinutes < 10) {
            currentMinutes = "0" + currentMinutes;
        }
        if (durationMinutes < 10) {
            durationMinutes = "0" + durationMinutes;
        }

        // Display the updated duration
        curr_time.textContent = currentMinutes + ":" + currentSeconds;
        total_duration.textContent = durationMinutes + ":" + durationSeconds;
    }
}

function seekTo() {
    // Calculate the seek position by the
    // percentage of the seek slider
    // and get the relative duration to the track
    let seekto = currPodcast.duration * (seek_slider.value / 100);

    // Set the current track position to the calculated seek position
    currPodcast.currentTime = seekto;
}

function backTenSeconds() {
    // Get current time
    let currTrackTime = currPodcast.currentTime;
    // Set time - 10 seconds
    let trackTimeMinusTen = currTrackTime - 10;
    // Check if resulting time is less than 0
    if (trackTimeMinusTen > 0) {
        currPodcast.currentTime = trackTimeMinusTen;
    }
    else {
        currPodcast.currentTime = 0;
    }
}

function forwardTenSeconds() {
    // Get current time
    let currTrackTime = currPodcast.currentTime;
    // Get total duration of track
    let currTrackDuration = currPodcast.duration;
    // Set time + 10 seconds
    let trackTimePlusTen = currTrackTime + 10;
    // Check if resulting time is more than total track duration
    if (trackTimePlusTen < currTrackDuration) {
        currPodcast.currentTime = trackTimePlusTen;
    }
    else {
        // Reset track;
        currPodcast.load();
        playpause_btn.innerHTML =
            '<i class="bi bi-play-circle" style="font-size: 3em;"></i>';
    }
}


// === Event listeners === //
playpause_btn.addEventListener("click", (e) => {
    if (!isPlaying) playPodcast();
    else pausePodcast();
});
