// api.js
const axios = require('axios');

/**
 * Get the last 'n' podcasts from the API
 * @param {number} n - Number of podcasts to retrieve
 * @returns {Promise} - Promise object representing the last 'n' podcasts
 * @throws {Error} - Error object
 * @example
 * // Get the last 4 podcasts
 * const n = 4;
 * getLastNPodcasts(n)
 *    .then(podcasts => {
 *       console.log('Last', n, 'podcasts:', podcasts);
 *   })
 *  .catch(error => {
 *      // Handle the error
 *     console.error('Error retrieving podcasts:', error);
 * }
 */ 
export function getLastNPodcasts(n) {
    const url = 'http://localhost:3001/podcasts';

    return axios.get(url)
        .then(response => {
            
            // Sort episodes in descending order by ID (assuming higher ID means more recent episode)
            const sortedEpisodes = response.data.sort((a, b) => b.id - a.id);
        
            // Slice the array to get the last 'n' episodes
            const lastNPodcasts = sortedEpisodes.slice(0, n);
            
            return lastNPodcasts;
        })
    .catch(error => {
        console.error('Error retrieving podcasts:', error);
        throw error;
    });
}


/**
 * Get all the podcasts from the API
 * @returns {Promise} - Promise object representing all the podcasts
 * @throws {Error} - Error object
 * @example
 * getAllPodcasts()
 *   .then(podcasts => {
 *      console.log('All podcasts:', podcasts);
 *  })
 * .catch(error => {
 *      // Handle the error
 *      console.error('Error retrieving podcasts:', error);
 * }
 */
export function getAllPodcasts() {
    const url = 'http://localhost:3001/podcasts';

    return axios.get(url)
        .then(response => {
            return response.data;
        })
    .catch(error => {
        console.error('Error retrieving podcasts:', error);
        throw error;
    });
}