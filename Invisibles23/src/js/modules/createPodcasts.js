import {PodcastPlayer} from './common/utils/PodcastPlayer.js';

// Create a new instance of PodcastPlayer
export function createPodcasts() {
    const linkArray = [
        'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3',
        'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
    ];

    // Get the container where the podcast players will be attached
    const playerContainer = document.getElementById('podcast-container');

    linkArray.forEach((link) => {
        let podcastPlayer = new PodcastPlayer(link);
        podcastPlayer.attachTo(playerContainer);
    });
}

