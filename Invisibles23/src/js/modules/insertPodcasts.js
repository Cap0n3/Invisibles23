/**
 * Instantiate the PodcastPlayer class and attach it to the container
 */
import {PodcastPlayer} from './common/utils/PodcastPlayer.js';
import {getAushaPodcasts} from './common/utils/api.js';

/**
 * Create the last podcasts for the homepage section
 * @returns {HTMLDivElement}
 */
export function homepagePodcasts() {
    const spinners = document.querySelectorAll('.load-spinner');
    const noPodcastsError = document.querySelectorAll('.no-podcast-error');

    // Show spinners while fetching the podcasts
    spinners.forEach((spinner) => {
        spinner.classList.remove('d-none');
    });

    // Get the last 4 podcasts from the API
    const n = 4; // Get the last 4 podcasts
    getAushaPodcasts(4)
        .then(podcasts => {
            // Hide the spinner
            spinners.forEach((spinner) => {
                spinner.classList.add('d-none');
            });

            //console.log('Last', n, 'podcasts:', podcasts);
            
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
            // Hide the spinner
            spinners.forEach((spinner) => {
                spinner.classList.add('d-none');
            });
            // Show an error message
            noPodcastsError.forEach((errorContainer) => {
                errorContainer.classList.remove('d-none');
            })
            // Handle the error
            console.error('Error retrieving podcasts:', error);
        });
}

/**
 * Create the podcasts for the podcasts page
 * @returns {HTMLDivElement}
 */
export function podcastsPage() {
    const spinner = document.getElementById('podcast-load-spin');
    const noPodcastsError = document.querySelectorAll('.no-podcast-error');

    // Show the spinner while fetching the podcasts
    spinner.classList.remove('d-none');
    
    // Get all the podcasts from the API
    getAushaPodcasts()
        .then(podcasts => {
            // Hide the spinner
            spinner.classList.add('d-none');

            // Assign the podcasts to the podcastArray
            const podcastArray = podcasts.data; 

            const playersPerPage = 4;
            let currentPage = 1;
            const container = document.getElementById('podcasts-section-container');
            
            const totalPlayers = podcastArray.length;
            const totalPages = Math.ceil(totalPlayers / playersPerPage);

            /**
             * Instantiate the players to display
             */
            function instantiatePlayers() {
                const startIndex = (currentPage - 1) * playersPerPage; // Determine the start index of the players to display
                const endIndex = startIndex + playersPerPage; // Determine the end index of the players to display
                const players = podcastArray.slice(startIndex, endIndex); // Get the players to display 
    
                // Clear container
                container.innerHTML = '';

                players.forEach(data => {
                    const player = createPlayerRows(data);
                    container.appendChild(player);
                });

                createPagination();
            }

            /**
             * Create the rows for the players and attach them to the container
             * @param {Object} podcastData
             * @returns {HTMLDivElement}
             */
            function createPlayerRows(podcastData) {
                let rowDiv = PodcastPlayer.generateHtmlTag('div', {
                    className: 'row mb-5',
                });

                let colDiv = PodcastPlayer.generateHtmlTag('div', {
                    className: 'col-12 d-flex justify-content-center',
                });

                let podcastPlayer = new PodcastPlayer(podcastData, 'big', 60);
                podcastPlayer.attachPodcastTo(colDiv);

                rowDiv.appendChild(colDiv);

                return rowDiv;
            }

            /**
             * Create the pagination
             * @returns {HTMLUListElement}
             */
            function createPagination() {
                const paginationNav = PodcastPlayer.generateHtmlTag('nav', {
                    'aria-label' :'Page navigation podcasts',
                    'className' : 'site-pagination'
                });

                const paginationUl = PodcastPlayer.generateHtmlTag('ul', {
                    className: 'pagination justify-content-center',
                });

                for (let i = 1; i <= totalPages; i++) {
                    const listElement = PodcastPlayer.generateHtmlTag('li', {
                        className: 'page-item',
                    });
                    const link = PodcastPlayer.generateHtmlTag('a', {
                        className: 'page-link',
                        href: '#',
                        text: i,
                    });
                    if (i === currentPage) {
                        link.classList.add('active');
                    }
                    link.addEventListener('click', () => {
                        currentPage = i;
                        instantiatePlayers();
                    });
                    listElement.appendChild(link);
                    paginationUl.appendChild(listElement);
                }
                paginationNav.appendChild(paginationUl);
                container.appendChild(paginationNav);
            }

            instantiatePlayers();
        })
        .catch(error => {
            // Hide the spinner
            spinner.classList.add('d-none');
            // Show an error message
            noPodcastsError.forEach((errorContainer) => {
                errorContainer.classList.remove('d-none');
            })
            // Handle the error
            console.error('Error retrieving podcasts:', error);
        });   
}