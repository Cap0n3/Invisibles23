import {PodcastPlayer} from './common/utils/PodcastPlayer.js';
import {getLastNPodcasts} from './common/utils/api.js';

// Create a new instance of PodcastPlayer
export function createPodcasts() {
    // Create array with object keys and values (id, link, title, description, date)
    // const podcastArray = [
    //     {
    //         id: 1,
    //         image_url: 'https://picsum.photos/id/234/300/300',
    //         audioUrl: 'https://audiofiles.ausha.co/fr-par/08/bd343e3ba57ebc8d934ecdc8c3787f95c89d7458.mp3?token=1685351870-64H8ZGVqXlI90mJE4JlGpf1T%2F%2BuN6RObI7ok3Z1wVl8%3D',
    //         name: 'Tamara et le syndrome du mal de débarquement, questionnée par de futur.es aide soignant.es',
    //         description: 'Certainly elsewhere my do allowance at. The address farther six hearted hundred towards husband. Are securing off occasion remember daughter replying. Held that feel his see own yet. Strangers ye to he sometimes propriety in. She right plate seven has. Bed who perceive judgment did marianne.',
    //         created_at: '2023-04-15T14:30:00+02:00',
    //     },
    //     {
    //         id: 2,
    //         image_url: 'https://picsum.photos/id/237/300/300',
    //         audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
    //         name: 'The Neverwritten Role Playing Game',
    //         description: 'One advanced diverted domestic sex repeated bringing you old. Possible procured her trifling laughter thoughts property she met way. Companions shy had solicitude favourable own. Which could saw guest man now heard but. Lasted my coming uneasy marked so should. Gravity letters it amongst herself dearest an windows by. Wooded ladies she basket season age her uneasy saw. Discourse unwilling am no described dejection incommode no listening of. Before nature his parish boy.',
    //         created_at: '2023-01-02T06:55:10+02:00',
    //     },
    //     {
    //         id: 3,
    //         image_url: 'https://picsum.photos/id/232/300/300',
    //         audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg',
    //         name: 'Epoq Lepidoptera',
    //         description: 'By spite about do of do allow blush. Additions in conveying or collected objection in. Suffer few desire wonder her object hardly nearer. Abroad no chatty others my silent an. Fat way appear denote who wholly narrow gay settle. Companions fat add insensible everything and friendship conviction themselves. Theirs months ten had add narrow own.',
    //         created_at: '2023-02-15T17:45:00+02:00',
    //     },
    //     {
    //         id: 4,
    //         image_url: 'https://picsum.photos/id/231/300/300',
    //         audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
    //         name: 'Playing Game Alt',
    //         description: 'If wandered relation no surprise of screened doubtful. Overcame no insisted ye of trifling husbands. Might am order hours on found. Or dissimilar companions friendship impossible at diminution. Did yourself carriage learning she man its replying. Sister piqued living her you enable mrs off spirit really. Parish oppose repair is me misery. Quick may saw style after money mrs.',
    //         created_at: '2023-09-05T09:45:00+02:00',
    //     },
    // ];

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

