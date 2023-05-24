import {PodcastPlayer} from './common/utils/PodcastPlayer.js';

// Create a new instance of PodcastPlayer
export function createPodcasts() {
    const linkArray = [
        'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3',
        'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
    ];

    // Create array with object keys and values (id, link, title, description, date)
    // const podcastArray = [
    //     {
    //         id: 1,
    //         link: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3',
    //         title: 'Sevish',
    //         description: 'Sevish song',
    //         date: '2021-09-01',
    //     },
    //     {
    //         id: 2,
    //         link: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
    //         title: 'The Neverwritten Role Playing Game',
    //         description: 'The Neverwritten Role Playing Game by Kangaroo MusiQue',
    //         date: '2021-09-02',
    //     },
    // ];

    // Get the container where the podcast players will be attached
    const playerContainer = document.getElementById('podcast-container');

    linkArray.forEach((link) => {
        let podcastPlayer = new PodcastPlayer(link);
        podcastPlayer.attachTo(playerContainer);
    });
}

