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
        this.isPlaying = false;
    }
  
    togglePlayback(targetBtn) {
        if (this.isPlaying) {
            this.pause(targetBtn);
        } else {
            this.play(targetBtn);
        }
    }
  
    play(targetBtn) {
        this.audioElement.play();
        this.isPlaying = true;
        targetBtn.className = 'playPause-btn bi bi-pause-circle';
    }
  
    pause(targetBtn) {
        this.audioElement.pause();
        this.isPlaying = false;
        targetBtn.className = 'playPause-btn bi bi-play-circle';
    }

    stop() {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
        this.isPlaying = false;
    }
  
    backTenSeconds() {
        this.audioElement.currentTime -= 10;
    }
  
    forwardTenSeconds() {
        this.audioElement.currentTime += 10;
    }

    seek(seekBarValue) {
        // Calculate the new time when the seek bar is changed
        let seekTo = this.audioElement.duration * (seekBarValue / 100); 
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

    // ======================== //
    // === Helper functions === //
    // ======================== //

    /**
     * Creates an HTML element dynamically.
     *
     * @param {string} tag - The HTML tag name of the element to create.
     * @param {Object} options - Options for configuring the element.
     * @param {string} [options.text=''] - The text content of the element.
     * @param {string} [options.html=''] - The inner HTML of the element.
     * @param {string} [options.className=''] - The class name to apply to the element.
     * @param {Object} [attributes={}] - Additional attributes to set on the element.
     * @returns {HTMLElement} The created HTML element.
     *
     * @example
     * // Create a simple div with nothing inside
     * const divElement = createHtmlTag('div');
     *
     * @example
     * // Create a p with text "Hello World!"
     * const pElement = createHtmlTag('p', { text: 'Hello World!' });
     *
     * @example
     * // Create an img with className "myImage" and src "www.mysource.com"
     * const imgElement = createHtmlTag('img', { className: 'myImage', src: 'www.mysource.com' });
     *
     * @example
     * // Create a div with custom innerHTML, className, and attributes
     * const customElement = createHtmlTag('div', {
     *   html: '<span>Custom Content</span>',
     *   className: 'myCustomClass',
     *   dataAttribute: 'example',
     * });
     */
    createHtmlTag(tag, {text = '', html = '', className = '', ...attributes } = {}) {
        const element = document.createElement(tag);
    
        if (text) {
          element.textContent = text;
        }

        if (html) {
            element.innerHTML = html;
        }
    
        if (className) {
          element.className = className;
        }
    
        Object.entries(attributes).forEach(([key, value]) => {
          element.setAttribute(key, value);
        });
    
        return element;
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
        // Create the podcast container
        const podcastContainer = this.createHtmlTag('div', { className: 'podcast-player' });

        // ===================================== //
        // === Column 1 of podcast container === //
        // ===================================== //
        const colOne = this.createHtmlTag('div', { className: 'col-one' });

        // == Podcast Image == //
        const image = this.createHtmlTag('img', { className: 'podcast-image', src: this.podcastImage });

        // == Mobile text group (hidden by default) == //
        const mobileTextGroup = this.createHtmlTag('div', { className: 'mobile-text-group hidden' });
        const mobileTitle = this.createHtmlTag('h3', {text: this.podcastTitle || 'Sans titre'});
        const mobileText = this.createHtmlTag('p', {text: this.podcastDescription || 'Pas de description disponible ...'});
        // Add title and text to mobile text group
        mobileTextGroup.appendChild(mobileTitle);
        mobileTextGroup.appendChild(mobileText);

        // == Controls container (where all podcast controls are) == //
        const controlsContainer = this.createHtmlTag('div', { className: 'player-controls' });
        
        // Play/Pause button
        const playPauseButton = this.createHtmlTag('i', { className: 'playPause-btn bi bi-play-circle' });
        playPauseButton.addEventListener('click', (e) => {
            this.togglePlayback(e.target);
        });

        // Backward and forward buttons
        const backButton = this.createHtmlTag('i', { className: 'bck-btn bi bi-arrow-counterclockwise' });
        backButton.addEventListener('click', () => {
            this.backTenSeconds();
        });

        const forwardButton = this.createHtmlTag('i', { className: 'fwd-btn bi bi-arrow-clockwise' });
        forwardButton.addEventListener('click', () => {
            this.forwardTenSeconds();
        });
        
        // Audio controls wrapper (back, play/pause, forward)
        const audioCTRLwrapper = this.createHtmlTag('div', { className: 'audio-ctrl-wrapper bg-danger' });
        audioCTRLwrapper.appendChild(backButton);
        audioCTRLwrapper.appendChild(playPauseButton);
        audioCTRLwrapper.appendChild(forwardButton);
        
        // Add audio controls wrapper to controls container
        controlsContainer.appendChild(audioCTRLwrapper);
        
        // == Seek bar == //
        const seekBarWrapper = this.createHtmlTag('div', { className: 'seek-bar-wrapper' });

        const seekBar = this.createHtmlTag('input', { 
            className: 'seek-bar', 
            type: 'range', 
            min: 0, 
            max: 100, 
            value: 0 
        });
        seekBar.addEventListener('input', (e) => {
            this.seek(e.target.value);
        });

        const currentTime = this.createHtmlTag('span', { className: 'current-time', text: '00:00' });
        const totalTime = this.createHtmlTag('span', { className: 'total-time', text: '00:00' });

        // Initialize totalTime text content on load
        this.audioElement.addEventListener('loadedmetadata', () => {
            let durationMinutes = Math.floor(this.audioElement.duration / 60);
            let durationSeconds = Math.floor(this.audioElement.duration - durationMinutes * 60);
            totalTime.textContent = this.formatTime(durationMinutes) + ':' + this.formatTime(durationSeconds);
        });

        // Update the seek bar as the audio plays
        this.audioElement.addEventListener('timeupdate', () => {
            if (!isNaN(this.audioElement.duration) && !isNaN(this.audioElement.currentTime)) {
                seekBar.value = (this.audioElement.currentTime / this.audioElement.duration) * 100;

                // Calculate the minutes and seconds of time left
                let currentMinutes = Math.floor(this.audioElement.currentTime / 60);
                let currentSeconds = Math.floor(this.audioElement.currentTime - currentMinutes * 60);
                let durationMinutes = Math.floor(this.audioElement.duration / 60);
                let durationSeconds = Math.floor(this.audioElement.duration - durationMinutes * 60);

                // Add a leading zero to the minutes and seconds if they are less than 10
                currentTime.textContent = this.formatTime(currentMinutes) + ':' + this.formatTime(currentSeconds);
                totalTime.textContent = this.formatTime(durationMinutes) + ':' + this.formatTime(durationSeconds);
            }
        });

        // Reset the seek bar when the audio ends
        this.audioElement.addEventListener('ended', () => {
                seekBar.value = 0;
                currentTime.textContent = '00:00';
                playPauseButton.className = 'playPause-btn bi bi-play-circle';
                this.isPlaying = false;
        });

        // Add seek bar to seek bar wrapper
        seekBarWrapper.appendChild(currentTime);
        seekBarWrapper.appendChild(seekBar);
        seekBarWrapper.appendChild(totalTime);
        
        // Add seek bar to controls container
        controlsContainer.appendChild(seekBarWrapper);

        // == Share button == //
        const shareButton = document.createElement('i');
        shareButton.className = 'bi bi-share';
        shareButton.setAttribute('data-bs-toggle', 'modal');
        shareButton.setAttribute('data-bs-target', `#shareModal_${this.podcastID}`);
        controlsContainer.appendChild(shareButton);

        // Share modal
        const shareModal = this.createHtmlTag('div', {
            className: 'modal fade',
            id: `shareModal_${this.podcastID}`,
            tabindex: '-1',
            'aria-labelledby': 'shareModalLabel',
            'aria-hidden': 'true'
        });
        
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
        // Attach event listeners to share icons & copy button
        shareButton.addEventListener('click', this.attachShareEventListeners.bind(this));

        // Download button
        const downloadButton = this.createHtmlTag('i', { className: 'bi bi-download' });
        
        downloadButton.addEventListener('click', async () => {
            try {
                const handle = await window.showSaveFilePicker();
                const writable = await handle.createWritable();
          
                const response = await fetch(this.audioUrl);
                const blob = await response.blob();
          
                const contentType = response.headers.get('Content-Type');
                const file = new File([blob], this.podcastTitle, { type: contentType });
          
                await writable.write(file);
                await writable.close();
            } catch (error) {
                console.error('Error while saving the file:', error);
            }
        });
        
        // Add download button to controls container
        controlsContainer.appendChild(downloadButton);

        // Append to colOne
        colOne.appendChild(image);
        colOne.appendChild(mobileTextGroup);
        colOne.appendChild(controlsContainer);
        colOne.appendChild(shareModal);

        // ===================================== //
        // === Column 2 of podcast container === //
        // ===================================== //
        const colTwo = this.createHtmlTag('div', { className: 'col-two' });

        // == Podcast Title and Text == //
        // Create a wrapper for the title and text (desktop only)
        const desktopTextWrapper = this.createHtmlTag('div', { className: 'desktop-text-wrapper' });

        // Title and text
        const title = this.createHtmlTag('h4', { text: this.podcastTitle || 'Sans titre' });
        const text = this.createHtmlTag('p', { text: this.podcastDescription || 'Pas de description disponible ...' });
        
        // Add title and text to desktop text wrapper
        desktopTextWrapper.appendChild(title);
        desktopTextWrapper.appendChild(text);
        
        // == Date and time == //
        // Create a wrapper for the date and time
        const dateWrapper = this.createHtmlTag('div', { className: 'date-wrapper' });
        
        const timeGroup = this.createHtmlTag('span', { 
            className: 'time-group', 
            html: `<i class="podcast-time-icon bi bi-clock"></i> ${this.podcastDateCreation.time}` || "Pas d'heure disponible ..." 
        });

        const dateSpan = this.createHtmlTag('span', {
            className: 'date-group',
            html: `<i class="podcast-date-icon bi bi-calendar"></i> ${this.podcastDateCreation.date}` || "Pas de date disponible ..."
        });

        // Add time and date to date wrapper
        dateWrapper.appendChild(timeGroup);
        dateWrapper.appendChild(dateSpan);

        // Append to colTwo
        colTwo.appendChild(desktopTextWrapper);
        colTwo.appendChild(dateWrapper);

        // === Append columns to podcast container === //
        podcastContainer.appendChild(colOne);
        podcastContainer.appendChild(colTwo);

        element.appendChild(podcastContainer);
    }
}