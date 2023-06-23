// api.js
const axios = require('axios');

/**
 * Get the last 'n' podcasts from the Ausha API.
 * 
 * @param {number} numberOfPodcasts - Number of podcasts to retrieve (if left empty, all podcasts are retrieved)
 * @returns {Promise} - Promise object representing the last 'n' podcasts
 * @throws {Error} - Error object
 * @example
 * // Get the last 4 podcasts
 * const n = 4;
 * getLastNPodcasts(n)
 *   .then(podcasts => {
 *     console.log('Last', n, 'podcasts:', podcasts);
 *  })
 * .catch(error => {
 *    // Handle the error
 *   console.error('Error retrieving podcasts:', error);
 * }
 */
export async function getAushaPodcasts(numberOfPodcasts = 0) {
    const url = "https://developers.ausha.co/v1/shows/44497/podcasts";

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AUSHA_API_TOKEN}`
    };

    try {
        const response = await axios.get(url, { headers });
        const allPodcasts = response.data;
        console.log('All podcasts:', allPodcasts);

        return (numberOfPodcasts > 0) ? allPodcasts.data.slice(0, numberOfPodcasts) : allPodcasts;
    } catch (error) {
        console.error('Error retrieving podcasts:', error);
        throw error;
    }
}

export function queryAPIAndCalculateTime() {
    const apiEndpoint = 'https://developers.ausha.co/v1/shows/44497/podcasts';
    const startTime = new Date().getTime(); // Get the current time in milliseconds
  
    fetch(apiEndpoint, {
      headers: {
        'Authorization': `Bearer ${process.env.AUSHA_API_TOKEN}` // Include the API token in the Authorization header
      }
    })
      .then(response => response.json())
      .then(data => {
        const endTime = new Date().getTime(); // Get the current time after the API request completes
        const elapsedTime = endTime - startTime; // Calculate the elapsed time in milliseconds
        console.log(`API query completed in ${elapsedTime} ms`);
        // Process the retrieved data here
      })
      .catch(error => {
        console.error('Error querying API:', error);
      });
  }
  