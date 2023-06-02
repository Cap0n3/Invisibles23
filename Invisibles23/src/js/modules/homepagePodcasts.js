import {PodcastPlayer} from './common/utils/PodcastPlayer.js';
import {getLastNPodcasts} from './common/utils/api.js';

/**
 * Create the last podcasts for the homepage section
 */
export function homepagePodcasts() {
    // Get the last 4 podcasts from the API
    const n = 4; // Get the last 4 podcasts
    getLastNPodcasts(n)
        .then(podcasts => {
            console.log('Last', n, 'podcasts:', podcasts);
            
            // Assign the podcasts to the podcastArray
            const podcastArray = podcasts;

            // Get the containers where the podcast players will be attached
            const playerContainers1 = document.querySelectorAll('.lastPodcast1');
            const playerContainers2 = document.querySelectorAll('.lastPodcast2');
            const playerContainers3 = document.querySelectorAll('.lastPodcast3');
            const playerContainers4 = document.querySelectorAll('.lastPodcast4');

            playerContainers1.forEach((playerContainer) => {
                let podcastPlayer = new PodcastPlayer(podcastArray[0]);
                podcastPlayer.attachPodcastTo(playerContainer);
            });
            
            playerContainers2.forEach((playerContainer) => {
                let podcastPlayer = new PodcastPlayer(podcastArray[1]);
                podcastPlayer.attachPodcastTo(playerContainer);
            });
            
            playerContainers3.forEach((playerContainer) => {
                let podcastPlayer = new PodcastPlayer(podcastArray[2]);
                podcastPlayer.attachPodcastTo(playerContainer);
            });

            playerContainers4.forEach((playerContainer) => {
                let podcastPlayer = new PodcastPlayer(podcastArray[3]);
                podcastPlayer.attachPodcastTo(playerContainer);
            });
        })
        .catch(error => {
            // Handle the error
            console.error('Error retrieving podcasts:', error);
        });
    
}

