/**
 * PodcastPlayer class to play audio files from a URL
 */
export class PodcastPlayer {
    constructor(audioUrl) {
        this.audioUrl = audioUrl;
        this.audioElement = new Audio(audioUrl);
        // Play button
        this.playButton = document.createElement('i');
        this.playButton.className = 'bi bi-play-circle';
        this.playButton.style.fontSize = '3em';
        this.playButton.addEventListener('click', this.togglePlayback.bind(this));
        this.isPlaying = false;
        // Back and forward buttons
        this.backButton = document.createElement('i');
        this.backButton.className = 'bi bi-arrow-counterclockwise';
        this.backButton.addEventListener('click', this.backTenSeconds.bind(this));

        this.forwardButton = document.createElement('i');
        this.forwardButton.className = 'bi bi-arrow-clockwise';
        this.forwardButton.addEventListener('click', this.forwardTenSeconds.bind(this));
        // Seek bar
        this.seekBar = document.createElement('input');
        this.seekBar.className = 'seek-bar';
        this.seekBar.type = 'range';
        this.seekBar.min = 0;
        this.seekBar.max = 100;
        this.seekBar.value = 0;
        this.currentTime = document.createElement('span');
        this.currentTime.className = 'current-time';
        this.currentTime.textContent = '00:00';
        this.totalTime = document.createElement('span');
        this.totalTime.className = 'total-time';
        this.totalTime.textContent = '00:00';
        

        // Initialize totalTime text content on load
        this.audioElement.addEventListener('loadedmetadata', () => {
            this.durationMinutes = Math.floor(this.audioElement.duration / 60);
            this.durationSeconds = Math.floor(this.audioElement.duration - this.durationMinutes * 60);
            this.totalTime.textContent = this.formatTime(this.durationMinutes) + ':' + this.formatTime(this.durationSeconds);
        });

        // update the seek bar as the audio plays
        this.audioElement.addEventListener('timeupdate', () => {
            if (!isNaN(this.audioElement.duration) && !isNaN(this.audioElement.currentTime)) {
                this.seekBar.value = (this.audioElement.currentTime / this.audioElement.duration) * 100;

                // Calculate the minutes and seconds of time left
                let currentMinutes = Math.floor(this.audioElement.currentTime / 60);
                let currentSeconds = Math.floor(this.audioElement.currentTime - currentMinutes * 60);
                let durationMinutes = Math.floor(this.audioElement.duration / 60);
                let durationSeconds = Math.floor(this.audioElement.duration - durationMinutes * 60);

                // Add a leading zero to the minutes and seconds if they are less than 10
                this.currentTime.textContent = this.formatTime(currentMinutes) + ':' + this.formatTime(currentSeconds);
                this.totalTime.textContent = this.formatTime(durationMinutes) + ':' + this.formatTime(durationSeconds);
            }
        });
    }
  
    togglePlayback() {
        if (this.isPlaying) {
            this.stop();
        } else {
            this.play();
        }
    }
  
    play() {
        this.audioElement.play();
        this.isPlaying = true;
        this.playButton.className = 'bi bi-pause-circle';
    }
  
    stop() {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
        this.isPlaying = false;
        this.playButton.className = 'bi bi-play-circle';
    }
  
    backTenSeconds() {
        this.audioElement.currentTime -= 10;
    }
  
    forwardTenSeconds() {
        this.audioElement.currentTime += 10;
    }
  
    formatTime(time) {
        return time < 10 ? '0' + time : time;
    }
  
    // Attach the player to an element in the DOM
    attachTo(element) {
        const podcastContainer = document.createElement('div');
        podcastContainer.className = 'podcast-player';
        
        // === Column 1 of podcast container === //
        const colOne = document.createElement('div');
        colOne.className = 'col-one';

        // Podcast Image
        const image = document.createElement('img');
        image.className = 'podcast-image';
        image.src = 'https://profilemagazine.com/wp-content/uploads/2020/04/Ajmere-Dale-Square-thumbnail.jpg';

        // Mobile text group (hidden by default)
        const mobileTextGroup = document.createElement('div');
        mobileTextGroup.className = 'mobile-text-group hidden';
        const mobileTitle = document.createElement('h3');
        mobileTitle.textContent = 'Podcast Title';
        const mobileText = document.createElement('p');
        mobileText.textContent =
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl quis ultrices ultricies, nunc nisl aliquam nunc, quis aliquet nisl nunc eget nisl.';

        mobileTextGroup.appendChild(mobileTitle);
        mobileTextGroup.appendChild(mobileText);

        // Player controls
        const playerControls = document.createElement('div');
        playerControls.className = 'player-controls';
        playerControls.appendChild(this.backButton);
        playerControls.appendChild(this.playButton);
        playerControls.appendChild(this.forwardButton);
        const seekGroup = document.createElement('div'); // seek bar and time
        seekGroup.className = 'seek-group';
        seekGroup.appendChild(this.currentTime);
        seekGroup.appendChild(this.seekBar);
        seekGroup.appendChild(this.totalTime);
        playerControls.appendChild(seekGroup);

        // Append to colOne
        colOne.appendChild(image);
        colOne.appendChild(mobileTextGroup);
        colOne.appendChild(playerControls);

        // === Column 2 of podcast container === //
        const colTwo = document.createElement('div');
        colTwo.className = 'col-two';

        // Podcast Title and Text
        const desktopTextGroup = document.createElement('div');
        desktopTextGroup.className = 'desktop-text-group';
        const title = document.createElement('h3');
        title.textContent = 'Podcast Title';

        const text = document.createElement('p');
        text.textContent =
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla euismod, nisl quis ultrices ultricies, nunc nisl aliquam nunc, quis aliquet nisl nunc eget nisl.';

        // Append to text groups
        desktopTextGroup.appendChild(title);
        desktopTextGroup.appendChild(text);
        

        // Append to colTwo
        colTwo.appendChild(desktopTextGroup);
        //colTwo.appendChild(mobileTextGroup);

        // === Append columns to podcast container === //
        podcastContainer.appendChild(colOne);
        podcastContainer.appendChild(colTwo);

        element.appendChild(podcastContainer);
    }
}