/**
 * PodcastPlayer class to play audio files from a URL.
 * @class
 * @example
 * // Create a new PodcastPlayer instance
 * let podcastPlayer = new PodcastPlayer(podcastData);
 * 
 * // Attach the podcast player to a container
 * podcastPlayer.attachPodcastTo(container);
 */
export class PodcastPlayer {
    /**
     * Creates an instance of PodcastPlayer.
     * @constructor
     * @param {Object} podcastData - The podcast data object
     * @param {string} podcastData.id - The podcast ID
     * @param {string} podcastData.image_url - The podcast image URL
     * @param {string} podcastData.name - The podcast title
     * @param {string} podcastData.html_description - The HTML podcast description
     * @param {string} podcastData.created_at - The podcast creation date
     * @param {string} podcastData.audio_url - The podcast audio URL
     * @param {string} [classPrefix=''] - The prefix for CSS classes to offer possibility of styling multiple players
     */
    constructor(podcastData, classPrefix = '', descriptionWordLimit = 30) {
        this.classPrefix = classPrefix; // Prefix for CSS classes
        this.descriptionWordLimit  = descriptionWordLimit; // Limit of words for the description
        this.podcastID = podcastData.id + "_" + Math.floor(Math.random() * (1000 - 1 + 1) + 1);
        this.podcastImage = podcastData.image_url;
        this.podcastTitle = podcastData.name;
        this.podcastDescription = podcastData.html_description;
        this.podcastDateCreation = this.convertDateFormat(podcastData.created_at);
        this.audioUrl = podcastData.audio_url;
        this.audioElement = new Audio(podcastData.audio_url);
        this.isPlaying = false;
        this.playPauseButton = PodcastPlayer.generateHtmlTag('i', { 
            className: 'playPause-btn bi bi-play-circle' 
        });
    }
  
    // ========= Podcast player methods ========= //

    /**
     * Toggles the playback state of the audio.
     * If currently playing, it pauses; if paused, it plays.
     */
    togglePlayback() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    /**
     * Plays the audio.
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/readyState|HTMLMediaElement.readyState}
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/HAVE_ENOUGH_DATA|HTMLMediaElement.HAVE_ENOUGH_DATA}
     */
    play() {
        // Display loading wheel on play button
        this.playPauseButton.className = 'load-icon';
        
        // HTMLMediaElement.HAVE_ENOUGH_DATA is always equal to 4 (see readyState link above)
        if (this.audioElement.readyState >= HTMLMediaElement.HAVE_ENOUGH_DATA) {
            // If audio is already loaded, remove the loading wheel and play the audio
            this.playPauseButton.className = 'playPause-btn bi bi-pause-circle';
            this.audioElement.play();
            this.isPlaying = true;
        } 
        else 
        {
            // Load the audio (Safari requires this otherwise it won't play)
            this.loadAudio();

            const playAfterLoad = () => {
                // Remove the event listener to avoid looping forever (ended calls loadAudio() again and triggers this event)
                this.audioElement.removeEventListener('canplaythrough', playAfterLoad);

                // Remove the loading wheel and play the audio
                console.log('Audio loaded.');
                this.playPauseButton.className = 'playPause-btn bi bi-pause-circle';
                this.audioElement.play();
                this.isPlaying = true;
            };

            this.audioElement.addEventListener('canplaythrough', playAfterLoad);

            // If the audio fails to load, handle the error
            this.audioElement.addEventListener('error', () => {
                // Remove the loading wheel and reset the play button
                this.playPauseButton.className = 'playPause-btn bi bi-play-circle';
                this.isPlaying = false;
                console.log('Error loading audio.');
            });
        }
    }
  
    pause() {
        this.audioElement.pause();
        this.isPlaying = false;
        this.playPauseButton.className = 'playPause-btn bi bi-play-circle';
    }

    // Not used (kept for reference)
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

    /**
     * Seeks the audio to the specified value.
     * @param {number} seekBarValue - The seek bar value (0-100)
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/seeked_event|HTMLMediaElement.seeked}
     */
    seek(seekBarValue) {
        // Show the loading indicator (spinner)
        this.playPauseButton.className = 'load-icon';
        // Calculate the new time when the seek bar is changed
        let seekTo = this.audioElement.duration * (seekBarValue / 100); 

        // Check if seekTo is a valid value (can happen if user slides real hard to the right with cursor)
        if (!isFinite(seekTo)) {
            console.log('Invalid seek time:', seekTo);
            seekTo = 0; // Set it to 0 as a default value
        }

        // Update the audio time to the new time
        this.audioElement.currentTime = seekTo;

        this.audioElement.addEventListener('seeked', () => {
            // Resume audio playback if it was playing before seeking
            if (this.isPlaying) {
                // show the play button
                this.playPauseButton.className = 'playPause-btn bi bi-pause-circle';
                this.audioElement.play();
            }
        });
    }

    /**
     * Sets the playback speed of the audio.
     * @param {number} speed - The playback speed
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/playbackRate|HTMLMediaElement.playbackRate}
     */
    setPlaybackSpeed(speed) {
        this.audioElement.playbackRate = speed;
    }
  
    loadAudio() {
        this.audioElement.load();
    }

    // ========= Helper methods ========= //

    formatTime(time) {
        return time < 10 ? '0' + time : time;
    }

    /**
     * Method to attach event listeners to the share icons
     * @param {string} linkToShare - The link to share
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/Window/open|Window.open()}
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/Window/open#Window_features|Window features}
     */
    attachShareEventListeners() {
        function shareOnFacebook(linkToShare) {
            // Open a new window with the Facebook share dialog
            window.open(
                `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(linkToShare)}`,
                'facebook-share-dialog',
                'width=800,height=600'
            );
        }

        function shareOnTwitter(linkToShare) {
            // Open a new window with the Twitter share dialog
            window.open(
                `https://twitter.com/intent/tweet?text=${encodeURIComponent(linkToShare)}`,
                'twitter-share-dialog',
                'width=800,height=600'
            );
        }

        function shareOnLinkedIn(linkToShare) {
            // Open a new window with the LinkedIn share dialog
            window.open(
                `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(linkToShare)}`,
                'linkedin-share-dialog',
                'width=800,height=600'
            );
        }

        function shareViaEmail(linkToShare) {
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
                        shareOnFacebook(linkToShare);
                        break;
                    case 'bi-twitter':
                        shareOnTwitter(linkToShare);
                        break;
                    case 'bi-linkedin':
                        shareOnLinkedIn(linkToShare);
                        break;
                    case 'bi-envelope':
                        shareViaEmail(linkToShare);
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

    /**
     * Static method to generate an HTML element dynamically.
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
     * const divElement = PodcastPlayer.generateHtmlTag('div');
     *
     * @example
     * // Create a p with text "Hello World!"
     * const pElement = PodcastPlayer.generateHtmlTag('p', { text: 'Hello World!' });
     *
     * @example
     * // Create an img with className "myImage" and src "www.mysource.com"
     * const imgElement = PodcastPlayer.generateHtmlTag('img', { className: 'myImage', src: 'www.mysource.com' });
     *
     * @example
     * // Create a div with custom innerHTML, className, and attributes
     * const customElement = PodcastPlayer.generateHtmlTag('div', {
     *   html: '<span>Custom Content</span>',
     *   className: 'myCustomClass',
     *   dataAttribute: 'example',
     * });
     * 
     * @example
     * // Since this is a static method, you can use it outside of an instance of PodcastPlayer class.
     * // Create a div outside of an instance of PodcastPlayer class :
     * 
     * const divElement = PodcastPlayer.generateHtmlTag('div', { className: 'myDiv' });
     * document.body.appendChild(divElement);
     */
    static generateHtmlTag(tag, {text = '', html = '', className = '', ...attributes } = {}) {
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
    
    /**
     * Converts a date string to a readable date format. It also adds leading zeros to the date and time values if needed.
     * For example, "2021-05-01T12:00:00" becomes "01/05/2021".
     * @param {*} dateString 
     * @returns 
     */
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
        const readableDate = `${formattedDay}/${formattedMonth}/${year}`;
        const readableTime = `${formattedHours}:${formattedMinutes}`;
        
        return {
          date: readableDate,
          time: readableTime
        };
    }

    /**
     * Limits the number of words in a string to avoid overflowing. It adds "..." at the end of the string if it is longer than the limit.
     */
    limitStringByWords(str, limit) {
        // Split the string into an array of words
        const words = str.split(' ');
      
        // Check if the number of words is already within the limit
        if (words.length <= limit) {
          return str;
        }
      
        // Create a new array with the limited number of words
        const limitedWords = words.slice(0, limit);
      
        // Join the limited words back into a string
        const limitedString = limitedWords.join(' ');
      
        return limitedString + " ...";
    }
  
    decodeHtmlEntities(str) {
        let txt = new DOMParser().parseFromString(str, "text/html");    
        return txt.documentElement.textContent;
    }    
    // ========= Element creation methods ========= //
    
    createPodcastImage() {
        return PodcastPlayer.generateHtmlTag('img', { 
            className: 'podcast-image', 
            src: this.podcastImage,
            title: `${this.podcastTitle}`,
            alt: `${this.podcastTitle}`
        });
    }

    /**
     * This method creates the text content of the podcast player.
     * 
     * @param {*} isMobile - If true, the text content will be created for mobile devices.
     * @returns 
     */
    createText(isMobile = false) {
        // Create a wrapper for the title and text (desktop only)
        const textDivWrapper = PodcastPlayer.generateHtmlTag('div', { 
            className: isMobile? 'mobile-text-group hidden' : 'desktop-text-wrapper'
        });
    
        // Title and text
        const title = PodcastPlayer.generateHtmlTag('h4', { 
            text: this.limitStringByWords(this.podcastTitle, 10) || 'Sans titre' 
        });
        const fullText = this.decodeHtmlEntities(this.podcastDescription) || 'Pas de description disponible ...';
        const limitedText = this.limitStringByWords(fullText, isMobile ? 25 : this.descriptionWordLimit);
    
        // Create text container
        const textContainer = PodcastPlayer.generateHtmlTag('div', {
            className: isMobile ? 'mobile-podcast-description' : 'podcast-description',
            html: limitedText
        });
    
        // Create show more/show less link
        const showMoreLink = PodcastPlayer.generateHtmlTag('a', { text: 'Voir plus' });
    
        let isFullText = false;
    
        const toggleText = () => {
            textContainer.innerHTML = isFullText ? limitedText : fullText;
            showMoreLink.textContent = isFullText ? 'Voir plus' : 'Voir moins';
            textContainer.appendChild(showMoreLink);
            isFullText = !isFullText;
        };
    
        showMoreLink.addEventListener('click', (event) => {
            event.preventDefault();
            toggleText();
        });
    
        // Add title, text container, and show more/show less link to desktop text wrapper
        textDivWrapper.appendChild(title);
        textDivWrapper.appendChild(textContainer);
        textContainer.appendChild(showMoreLink);
        //textDivWrapper.appendChild(showMoreLink);
    
        return textDivWrapper;
    }    

    createAudioNavCtrl() {
        // Play/Pause button
        this.playPauseButton.addEventListener('click', (e) => {
            this.togglePlayback();
        });

        // Backward and forward buttons
        const backButton = PodcastPlayer.generateHtmlTag('i', { className: 'bck-btn bi bi-arrow-counterclockwise' });
        backButton.addEventListener('click', () => {
            this.backTenSeconds();
        });

        const forwardButton = PodcastPlayer.generateHtmlTag('i', { className: 'fwd-btn bi bi-arrow-clockwise' });
        forwardButton.addEventListener('click', () => {
            this.forwardTenSeconds();
        });
        
        // Audio controls wrapper (back, play/pause, forward)
        const audioControls = PodcastPlayer.generateHtmlTag('div', { className: 'audio-ctrl-wrapper' });
        audioControls.appendChild(backButton);
        audioControls.appendChild(this.playPauseButton);
        audioControls.appendChild(forwardButton);

        return audioControls;
    }

    createSeekBar() {
        // == Seek bar == //
        const seekBarWrapper = PodcastPlayer.generateHtmlTag('div', { className: 'seek-bar-wrapper' });

        const seekBar = PodcastPlayer.generateHtmlTag('input', { 
            className: 'seek-bar', 
            type: 'range', 
            min: 0, 
            max: 100, 
            value: 0 
        });

        // Update the seek bar when it is seeked
        seekBar.addEventListener('input', (e) => {
            this.seek(e.target.value);
        });

        const currentTime = PodcastPlayer.generateHtmlTag('span', { className: 'current-time', text: '00:00' });
        const totalTime = PodcastPlayer.generateHtmlTag('span', { className: 'total-time', text: '00:00' });
        
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
                console.log('Audio ended');
                seekBar.value = 0;
                currentTime.textContent = '00:00';
                this.playPauseButton.className = 'playPause-btn bi bi-play-circle';
                this.isPlaying = false;
                this.loadAudio(); // Reset the audio element (for Firefox)
        });

        // Add seek bar to seek bar wrapper
        seekBarWrapper.appendChild(currentTime);
        seekBarWrapper.appendChild(seekBar);
        seekBarWrapper.appendChild(totalTime);

        return seekBarWrapper;
    }

    createShareButton() {
        const shareButton = document.createElement('i');
        shareButton.className = 'bi bi-share';
        shareButton.setAttribute('data-bs-toggle', 'modal');
        shareButton.setAttribute('data-bs-target', `#shareModal_${this.podcastID}`);

        return shareButton;
    }

    createSpeedButton() {
        const speedButton = PodcastPlayer.generateHtmlTag('button', { 
            className: 'speed-btn', 
            type: 'button',
            'data-bs-toggle': 'dropdown',
            'aria-expanded': 'false'
        });
        const speedIcon = PodcastPlayer.generateHtmlTag('i', { className: 'bi bi-speedometer2' });
        const speedOptions = [0.5, 1, 1.5, 2];
        
        const speedMenu = PodcastPlayer.generateHtmlTag('ul', { className: 'speed-menu dropdown-menu' });
        
        speedOptions.forEach((speed) => {
            const speedItem = PodcastPlayer.generateHtmlTag('li');
            const speedLink = PodcastPlayer.generateHtmlTag('a', { 
                text: speed + 'x', 
                className: 'dropdown-item'
            });
        
            speedLink.addEventListener('click', () => {
                this.setPlaybackSpeed(speed);
            });
        
            speedItem.appendChild(speedLink);
            speedMenu.appendChild(speedItem);
        });
        
        speedButton.appendChild(speedIcon);
        speedButton.appendChild(speedMenu);
        
        return speedButton;
    }

    createShareModal() {
        const shareModal = PodcastPlayer.generateHtmlTag('div', {
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
                            <i class="share-icons-${this.podcastID} modal-social-icons bi bi-facebook"></i>
                            <i class="share-icons-${this.podcastID} modal-social-icons bi bi-twitter"></i>
                            <i class="share-icons-${this.podcastID} modal-social-icons bi bi-linkedin"></i>
                            <i class="share-icons-${this.podcastID} modal-social-icons bi bi-envelope"></i>
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

        return shareModal;
    }

    createDownloadButton() {
        const downloadButton = PodcastPlayer.generateHtmlTag('i', { className: 'bi bi-download' });
        
        downloadButton.addEventListener('click', async () => {
            // Cool experimental feature, but not supported by all browsers yet, keep an eye on it
            // https://web.dev/file-system-access/
            
            // try {
            //     const options = {
            //         suggestedName: this.podcastTitle, // Set the initial file name
            //         types: [{
            //                 description: 'Audio Files',
            //                 accept: {
            //                     'audio/*': ['.mp3', '.wav'] // Set the accepted file types
            //                 }
            //         }]
            //     };
            //     const handle = await window.showSaveFilePicker(options);
            //     const writable = await handle.createWritable();
          
            //     const response = await fetch(this.audioUrl);
            //     const blob = await response.blob();
                
            //     const contentType = response.headers.get('Content-Type');
            //     const file = new File([blob], this.podcastTitle, { type: contentType });
          
            //     await writable.write(file);
            //     await writable.close();
            // } catch (error) {
            //     console.error('Error while saving the file:', error);
            // }

            // Best solution for now
            try {
                const response = await fetch(this.audioUrl);
                const blob = await response.blob();
            
                const contentType = response.headers.get('Content-Type');
                const file = new File([blob], this.podcastTitle, { type: contentType });
            
                const downloadUrl = URL.createObjectURL(file);
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.download = this.podcastTitle; // Set the desired file name
                link.click();
            
                URL.revokeObjectURL(downloadUrl);
            } catch (error) {
                console.error('Error while saving the file:', error);
            }
        });

        return downloadButton;
    }

    createDateTimeWrapper() {
        // Create a wrapper for the date and time
        const dateWrapper = PodcastPlayer.generateHtmlTag('div', { className: 'date-wrapper' });
        
        const timeGroup = PodcastPlayer.generateHtmlTag('span', { 
            className: 'time-group', 
            html: `<i class="podcast-time-icon bi bi-clock"></i> ${this.podcastDateCreation.time}` || "Pas d'heure disponible ..." 
        });

        const dateSpan = PodcastPlayer.generateHtmlTag('span', {
            className: 'date-group',
            html: `<i class="podcast-date-icon bi bi-calendar"></i> ${this.podcastDateCreation.date}` || "Pas de date disponible ..."
        });

        // Add time and date to date wrapper
        dateWrapper.appendChild(timeGroup);
        dateWrapper.appendChild(dateSpan);

        return dateWrapper;
    }

    // ========= Main Method (attach podcast to DOM) ========= //

    /**
     * Attach the podcast to the DOM.
     * @example
     * const podcast = new PodcastPlayer({ ... });
     * podcast.attachPodcastTo(document.body);
     * @param {*} element 
     */
    attachPodcastTo(element) {
        // === Create main podcast containers === //
        const podcastContainer = PodcastPlayer.generateHtmlTag('div', { 
            className: `${this.classPrefix ? this.classPrefix + '-' : ''}podcast-player` 
        });
        const colOne = PodcastPlayer.generateHtmlTag('div', { className: 'col-one' });
        const colTwo = PodcastPlayer.generateHtmlTag('div', { className: 'col-two' });
        
        // === Create all podcast elements & attach listeners (if needed) === //
        const image = this.createPodcastImage(); // Podcast image
        const mobileTextWrapper = this.createText(true);  // Podcast title and text (mobile)
        const desktopTextWrapper = this.createText(); // Podcast title and text (desktop)
        const audioNavControls = this.createAudioNavCtrl(); // Audio navigation controls (back, play/pause, forward)
        const seekBar = this.createSeekBar(); // Seek bar
        const shareButton = this.createShareButton(); // Share button
        shareButton.addEventListener('click', this.attachShareEventListeners.bind(this)); // Attach event listeners to share button
        const shareModal = this.createShareModal();  // Share modal
        const downloadButton = this.createDownloadButton(); // Download button
        const speedButton = this.createSpeedButton(); // Speed button
        const dateTimeWrapper = this.createDateTimeWrapper(); // Date and time
        const mobileDateTimeWrapper = dateTimeWrapper.cloneNode(true);
        mobileDateTimeWrapper.classList.add('hidden'); // Hide date and time on mobile
        
        // Controls container (where all audio controls are) //
        const controlsContainer = PodcastPlayer.generateHtmlTag('div', { className: 'player-controls' });        
        controlsContainer.appendChild(audioNavControls);    
        controlsContainer.appendChild(seekBar);
        
        // Share container
        const shareContainer = PodcastPlayer.generateHtmlTag('div', { className: 'share-container' });
        shareContainer.appendChild(speedButton);
        shareContainer.appendChild(shareButton);
        shareContainer.appendChild(shareModal);
        shareContainer.appendChild(downloadButton);
            
        // === Append all elements to columns === // 
        // Column 1
        colOne.appendChild(image);
        colOne.appendChild(mobileTextWrapper); // Only visible on mobile
        colOne.appendChild(controlsContainer);
        colOne.appendChild(shareContainer);
        colOne.appendChild(mobileDateTimeWrapper); // Only visible on mobile

        // Column 2
        colTwo.appendChild(desktopTextWrapper);
        colTwo.appendChild(dateTimeWrapper);

        // === Finally append columns to podcast container === //
        podcastContainer.appendChild(colOne);
        podcastContainer.appendChild(colTwo);
        element.appendChild(podcastContainer);
    }
}