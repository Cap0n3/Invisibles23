import {PodcastPlayer} from './common/utils/PodcastPlayer.js';
import {getAllPodcasts} from './common/utils/api.js';


export function podcastsPage() {
    // Get all the podcasts from the API
    getAllPodcasts()
        .then(podcasts => {
            
            const podcastArray = podcasts; // Assign the podcasts to the podcastArray
            podcastArray.reverse(); // Reverse the array so the most recent podcasts are displayed first

            console.log('All podcasts:', podcasts);
            
            const playersPerPage = 2;
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
                    className: 'row justify-content-center mb-5',
                });

                let colDiv = PodcastPlayer.generateHtmlTag('div', {
                    className: 'col-12',
                });

                let podcastPlayer = new PodcastPlayer(podcastData);
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
                    // const link = document.createElement('a');
                    // link.href = '#';
                    // link.textContent = i;
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
            // Handle the error
            console.error('Error retrieving podcasts:', error);
        });   
}