/**
 * PodcastPlayer class to play audio files from a URL
 */
export class PodcastPlayer {
    constructor(podcastData) {
        this.podcastID = podcastData.id;
        this.podcastImage = podcastData.image_url;
        this.podcastTitle = podcastData.title;
        this.podcastDescription = podcastData.description;
        this.podcastDateCreation = this.convertDateFormat(podcastData.created_at);
        this.audioUrl = podcastData.audioUrl;
        // Create the <audio> element
        this.audioElement = new Audio(podcastData.audioUrl);
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
        this.seekBar.addEventListener('input', this.seek.bind(this));
        

        // Initialize totalTime text content on load
        this.audioElement.addEventListener('loadedmetadata', () => {
            this.durationMinutes = Math.floor(this.audioElement.duration / 60);
            this.durationSeconds = Math.floor(this.audioElement.duration - this.durationMinutes * 60);
            this.totalTime.textContent = this.formatTime(this.durationMinutes) + ':' + this.formatTime(this.durationSeconds);
        });

        // Update the seek bar as the audio plays
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

        // Reset the seek bar when the audio ends
        this.audioElement.addEventListener('ended', () => {
                this.seekBar.value = 0;
                this.currentTime.textContent = '00:00';
                this.totalTime.textContent = '00:00';
                this.isPlaying = false;
                this.playButton.className = 'bi bi-play-circle';
            }
        );
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

    seek() {
        // Calculate the new time when the seek bar is changed
        let seekTo = this.audioElement.duration * (this.seekBar.value / 100); 
        // Update the audio time to the new time
        this.audioElement.currentTime = seekTo;
    }
  
    formatTime(time) {
        return time < 10 ? '0' + time : time;
    }

    // Function to attach event listeners to the share icons
    attachShareEventListeners() {
        const shareIcons = document.querySelectorAll(`.share-icons-${this.podcastID}`);
        const copyLinkButton = document.getElementById(`copyButton_${this.podcastID}`);
        
        shareIcons.forEach((icon) => {
            icon.addEventListener('click', (event) => {
                const linkToShare = this.audioUrl;
                const icon = event.target;
                // Get last class name of the icon (the social media platform)
                const socialMedia = icon.classList[icon.classList.length - 1];
                switch (socialMedia) {
                    case 'bi-facebook':
                        this.shareOnFacebook(linkToShare);
                        break;
                    case 'bi-twitter':
                        this.shareOnTwitter(linkToShare);
                        break;
                    case 'bi-linkedin':
                        this.shareOnLinkedIn(linkToShare);
                        break;
                    case 'bi-envelope':
                        this.shareViaEmail(linkToShare);
                        break;
                    default:
                        break;
                }
            });
        });

        copyLinkButton.addEventListener('click', () => {
            const linkToShare = this.audioUrl;
            // navigator.clipboard.writeText(linkToShare);
            
            navigator.clipboard.writeText(linkToShare).then(
                () => {
                    /* clipboard successfully set */
                    console.log("clipboard successfully set");
                    copyLinkButton.textContent = 'Copié !';
                    setTimeout(() => {
                        copyLinkButton.textContent = 'Copier';
                    }, 2000);
                },
                () => {
                    /* clipboard write failed */
                    console.log("clipboard write failed");
                }
            );
            console.log(this.audioUrl);
        });
    }

    // Function to share the podcast on Facebook
    shareOnFacebook(linkToShare) {
        // Open a new window with the Facebook share dialog
        window.open(
            `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(linkToShare)}`,
            'facebook-share-dialog',
            'width=800,height=600'
        );
    }

    // Function to share the podcast on Twitter
    shareOnTwitter(linkToShare) {
        // Open a new window with the Twitter share dialog
        window.open(
            `https://twitter.com/intent/tweet?text=${encodeURIComponent(linkToShare)}`,
            'twitter-share-dialog',
            'width=800,height=600'
        );
    }

    // Function to share the podcast on LinkedIn
    shareOnLinkedIn(linkToShare) {
        // Open a new window with the LinkedIn share dialog
        window.open(
            `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(linkToShare)}`,
            'linkedin-share-dialog',
            'width=800,height=600'
        );
    }    

    // Function to share the podcast via email
    shareViaEmail(linkToShare) {
        const subject = 'Le Podcast "Les Invisibles" de Tamara Pellegrini';
        const body = `Je souhaiterais partager ce podcast avec toi :\n\n ${linkToShare}`;
        const url = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        window.location.href = url;
        /**
         * Reload the page after email client is opened to avoid error "Not allowed to launch mailto because a user gesture is required" (security issue)
         * when the user tries to share different podcasts several times in a row (youtube has a better solution with a new tab opening but I can't find it).
         * When user share several podcasts in a row, the first share works but the following ones don't and first request is sent again instead.
         */
        window.location.reload();
    }

    convertDateFormat(dateString) {
        const date = new Date(dateString);
        
        // Extracting the components
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        
        // Padding the values with leading zeros if needed
        const formattedMonth = month.toString().padStart(2, '0');
        const formattedDay = day.toString().padStart(2, '0');
        const formattedHours = hours.toString().padStart(2, '0');
        const formattedMinutes = minutes.toString().padStart(2, '0');
        // const formattedSeconds = seconds.toString().padStart(2, '0');
        
        // Creating the readable date and time string
        const readableDate = `${formattedDay}-${formattedMonth}-${year}`;
        const readableTime = `${formattedHours}:${formattedMinutes}`;
        
        return {
          date: readableDate,
          time: readableTime
        };
    }
  
    // =============================================== //
    // === Attach the podcast player to an element === //
    // =============================================== //
    attachTo(element) {
        const podcastContainer = document.createElement('div');
        podcastContainer.className = 'podcast-player';
        
        // ===================================== //
        // === Column 1 of podcast container === //
        // ===================================== //
        const colOne = document.createElement('div');
        colOne.className = 'col-one';

        // Podcast Image
        const image = document.createElement('img');
        image.className = 'podcast-image';
        image.src = this.podcastImage;

        // Mobile text group (hidden by default)
        const mobileTextGroup = document.createElement('div');
        mobileTextGroup.className = 'mobile-text-group hidden';
        const mobileTitle = document.createElement('h3');
        mobileTitle.textContent = this.podcastTitle || 'Sans titre';
        const mobileText = document.createElement('p');
        mobileText.textContent = this.podcastDescription || 'Pas de description disponible ...';

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

        // Share button
        const shareButton = document.createElement('i');
        shareButton.className = 'bi bi-share';
        shareButton.setAttribute('data-bs-toggle', 'modal');
        shareButton.setAttribute('data-bs-target', `#shareModal_${this.podcastID}`);
        playerControls.appendChild(shareButton);

        // Share modal
        const shareModal = document.createElement('div');
        shareModal.className = 'modal fade';
        shareModal.setAttribute('id', `shareModal_${this.podcastID}`);
        shareModal.setAttribute('tabindex', '-1');
        shareModal.setAttribute('aria-labelledby', 'shareModalLabel');
        shareModal.setAttribute('aria-hidden', 'true');
        
        shareModal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title" id="shareModalLabel">Partagez le podcast !</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="d-flex gap-5 justify-content-center">
                            <i class="share-icons-${this.podcastID} social-icons bi bi-facebook"></i>
                            <i class="share-icons-${this.podcastID} social-icons bi bi-twitter"></i>
                            <i class="share-icons-${this.podcastID} social-icons bi bi-linkedin"></i>
                            <i class="share-icons-${this.podcastID} social-icons bi bi-envelope"></i>
                        </div>
                        <hr />
                        <div class="d-flex justify-content-center gap-3">   
                            <input type="text" class="share-link form-control" value="${this.audioUrl}" />
                            <button class="btn btn-primary copy-button" id="copyButton_${this.podcastID}">Copier</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        // Attach event listeners to share icons
        shareButton.addEventListener('click', this.attachShareEventListeners.bind(this));


        // Append to colOne
        colOne.appendChild(image);
        colOne.appendChild(mobileTextGroup);
        colOne.appendChild(playerControls);
        colOne.appendChild(shareModal);

        // ===================================== //
        // === Column 2 of podcast container === //
        // ===================================== //
        const colTwo = document.createElement('div');
        colTwo.className = 'col-two';

        // Podcast Title and Text
        const desktopTextGroup = document.createElement('div');
        desktopTextGroup.className = 'desktop-text-group';
        const title = document.createElement('h4');
        title.textContent = this.podcastTitle || 'Sans titre';
        const text = document.createElement('p');
        text.textContent = this.podcastDescription || 'Pas de description disponible ...';
        desktopTextGroup.appendChild(title);
        desktopTextGroup.appendChild(text);
        
        const dateContainer = document.createElement('div');
        dateContainer.className = 'date-container d-flex justify-content-between';
        const timeSpan = document.createElement('span');
        timeSpan.classList.add('time-group');
        timeSpan.innerHTML = `<i class="podcast-time-icon bi bi-clock"></i> ${this.podcastDateCreation.time}` || "Pas d'heure disponible ...";
        const dateSpan = document.createElement('span');
        dateSpan.classList.add('date-group');
        dateSpan.innerHTML = `<i class="podcast-date-icon bi bi-calendar"></i> ${this.podcastDateCreation.date}` || "Pas de date disponible ...";
        dateContainer.appendChild(timeSpan);
        dateContainer.appendChild(dateSpan);

        // Append to colTwo
        colTwo.appendChild(desktopTextGroup);
        colTwo.appendChild(dateContainer);

        // === Append columns to podcast container === //
        podcastContainer.appendChild(colOne);
        podcastContainer.appendChild(colTwo);

        element.appendChild(podcastContainer);
    }
}