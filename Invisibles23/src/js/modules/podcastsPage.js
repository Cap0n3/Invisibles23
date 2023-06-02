import {PodcastPlayer} from './common/utils/PodcastPlayer.js';
import {getAllPodcasts} from './common/utils/api.js';

export function podcastsPage() {
    // Get all the podcasts from the API
    getAllPodcasts()
        .then(podcasts => {
            console.log('All podcasts:', podcasts);
            
            // Assign the podcasts to the podcastArray
            const podcastArray = podcasts;

            // Get the containers where the podcast players will be attached
            // const playerContainers = document.querySelectorAll('.podcastPlayer');

            // playerContainers.forEach((playerContainer, index) => {
            //     let podcastPlayer = new PodcastPlayer(podcastArray[index]);
            //     podcastPlayer.attachPodcastTo(playerContainer);
            // });
        })
        .catch(error => {
            // Handle the error
            console.error('Error retrieving podcasts:', error);
        });   
}