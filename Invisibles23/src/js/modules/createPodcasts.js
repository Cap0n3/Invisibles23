import {PodcastPlayer} from './common/utils/PodcastPlayer.js';

// Create a new instance of PodcastPlayer
export function createPodcasts() {
    // const linkArray = [
    //     'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3',
    //     'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
    // ];

    // Create array with object keys and values (id, link, title, description, date)
    const podcastArray = [
        {
            id: 1,
            image_url: 'https://picsum.photos/id/234/300/300',
            audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3',
            title: 'Sevish',
            description: 'Certainly elsewhere my do allowance at. The address farther six hearted hundred towards husband. Are securing off occasion remember daughter replying. Held that feel his see own yet. Strangers ye to he sometimes propriety in. She right plate seven has. Bed who perceive judgment did marianne.',
            created_at: '2023-04-15T14:30:00+02:00',
        },
        {
            id: 2,
            image_url: 'https://picsum.photos/id/237/300/300',
            audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
            title: 'The Neverwritten Role Playing Game',
            description: 'One advanced diverted domestic sex repeated bringing you old. Possible procured her trifling laughter thoughts property she met way. Companions shy had solicitude favourable own. Which could saw guest man now heard but. Lasted my coming uneasy marked so should. Gravity letters it amongst herself dearest an windows by. Wooded ladies she basket season age her uneasy saw. Discourse unwilling am no described dejection incommode no listening of. Before nature his parish boy.',
            created_at: '2022-09-05T08:45:00+02:00',
        },
    ];

    // Get the container where the podcast players will be attached
    const playerContainer = document.getElementById('podcast-container');

    podcastArray.forEach((podcastData) => {
        let podcastPlayer = new PodcastPlayer(podcastData);
        podcastPlayer.attachTo(playerContainer);
    });
}

