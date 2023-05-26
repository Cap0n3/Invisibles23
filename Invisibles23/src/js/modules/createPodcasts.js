import {PodcastPlayer} from './common/utils/PodcastPlayer.js';

// Create a new instance of PodcastPlayer
export function createPodcasts() {
    // Create array with object keys and values (id, link, title, description, date)
    const podcastArray = [
        {
            id: 1,
            image_url: 'https://picsum.photos/id/234/300/300',
            audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3',
            title: 'Tamara et le syndrome du mal de débarquement, questionnée par de futur.es aide soignant.es',
            description: 'Certainly elsewhere my do allowance at. The address farther six hearted hundred towards husband. Are securing off occasion remember daughter replying. Held that feel his see own yet. Strangers ye to he sometimes propriety in. She right plate seven has. Bed who perceive judgment did marianne.',
            created_at: '2023-04-15T14:30:00+02:00',
        },
        {
            id: 2,
            image_url: 'https://picsum.photos/id/237/300/300',
            audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
            title: 'The Neverwritten Role Playing Game',
            description: 'One advanced diverted domestic sex repeated bringing you old. Possible procured her trifling laughter thoughts property she met way. Companions shy had solicitude favourable own. Which could saw guest man now heard but. Lasted my coming uneasy marked so should. Gravity letters it amongst herself dearest an windows by. Wooded ladies she basket season age her uneasy saw. Discourse unwilling am no described dejection incommode no listening of. Before nature his parish boy.',
            created_at: '2023-01-02T06:55:10+02:00',
        },
        {
            id: 3,
            image_url: 'https://picsum.photos/id/232/300/300',
            audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg',
            title: 'Epoq Lepidoptera',
            description: 'By spite about do of do allow blush. Additions in conveying or collected objection in. Suffer few desire wonder her object hardly nearer. Abroad no chatty others my silent an. Fat way appear denote who wholly narrow gay settle. Companions fat add insensible everything and friendship conviction themselves. Theirs months ten had add narrow own.',
            created_at: '2023-02-15T17:45:00+02:00',
        },
        {
            id: 4,
            image_url: 'https://picsum.photos/id/231/300/300',
            audioUrl: 'http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3',
            title: 'Playing Game Alt',
            description: 'If wandered relation no surprise of screened doubtful. Overcame no insisted ye of trifling husbands. Might am order hours on found. Or dissimilar companions friendship impossible at diminution. Did yourself carriage learning she man its replying. Sister piqued living her you enable mrs off spirit really. Parish oppose repair is me misery. Quick may saw style after money mrs.',
            created_at: '2023-09-05T09:45:00+02:00',
        },
    ];

    // Get the container where the podcast players will be attached
    // const playerContainer = document.getElementById('podcast-container');

    // podcastArray.forEach((podcastData) => {
    //     let podcastPlayer = new PodcastPlayer(podcastData);
    //     podcastPlayer.attachPodcastTo(playerContainer);
    // });

    // Get the container where the podcast players will be attached
    const playerContainer1 = document.getElementById('lastPodcast1');
    const playerContainer2 = document.getElementById('lastPodcast2');
    const playerContainer3 = document.getElementById('lastPodcast3');
    const playerContainer4 = document.getElementById('lastPodcast4');

    // add them to array
    const playerContainers = [playerContainer1, playerContainer2, playerContainer3, playerContainer4];

    // add podcast to each container
    podcastArray.forEach((podcastData, index) => {
        let podcastPlayer = new PodcastPlayer(podcastData);
        podcastPlayer.attachPodcastTo(playerContainers[index]);
    });

    
}

