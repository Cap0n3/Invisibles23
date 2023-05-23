// /**
//  * PodcastPlayer class to play audio files from a URL
//  */
// export class PodcastPlayer {
//     constructor(audioUrl) {
//         this.audioUrl = audioUrl;
//         this.audioElement = new Audio(audioUrl);
//         //this.playButton = document.createElement('button');
//         //this.playButton.textContent = 'Play';
//         this.playButton = document.createElement('i');
//         this.playButton.className = 'bi bi-play-circle';
//         this.playButton.style.fontSize = '3em';
//         this.playButton.addEventListener('click', this.togglePlayback.bind(this));
//         this.isPlaying = false;
//     }

//     togglePlayback() {
//         if (this.isPlaying) {
//             this.stop();
//         } else {
//             this.play();
//         }
//     }

//     play() {
//         this.audioElement.play();
//         this.isPlaying = true;
//         this.playButton.className = 'bi bi-pause-circle';
//     }

//     stop() {
//         this.audioElement.pause();
//         this.audioElement.currentTime = 0;
//         this.isPlaying = false;
//         this.playButton.className = 'bi bi-play-circle';
//     }

//     // Attach the player to an element in the DOM
//     attachTo(element) {
//         const div = document.createElement('div');
//         div.className = 'podcast-player';
//         div.appendChild(this.playButton);
//         element.appendChild(div);
//     }
// }


/**
 * PodcastPlayer class to play audio files from a URL
 */
export class PodcastPlayer {
    constructor(audioUrl) {
        this.audioUrl = audioUrl;
        this.audioElement = new Audio(audioUrl);
        this.playButton = document.createElement('i');
        this.playButton.className = 'bi bi-play-circle';
        this.playButton.style.fontSize = '3em';
        this.playButton.addEventListener('click', this.togglePlayback.bind(this));
        this.isPlaying = false;

        this.backButton = document.createElement('i');
        this.backButton.className = 'bi bi-arrow-counterclockwise';
        this.backButton.addEventListener('click', this.backTenSeconds.bind(this));

        this.forwardButton = document.createElement('i');
        this.forwardButton.className = 'bi bi-arrow-clockwise';
        this.forwardButton.addEventListener('click', this.forwardTenSeconds.bind(this));
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

    // Attach the player to an element in the DOM
    attachTo(element) {
        const div = document.createElement('div');
        div.className = 'podcast-player';
        div.appendChild(this.backButton);
        div.appendChild(this.playButton);
        div.appendChild(this.forwardButton);
        element.appendChild(div);
    }
}
