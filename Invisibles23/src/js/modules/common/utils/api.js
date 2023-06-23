// api.js
const axios = require('axios');
const mailchimp = require('@mailchimp/mailchimp_marketing');

// ======================== //
// === Aush Podcast API === //
// ======================== //


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

/**
 * Test the API query and calculate the elapsed time.
 */
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

// ===================== //
// === Mailchimp API === //
// ===================== //

mailchimp.setConfig({
    apiKey: process.env.MAILCHIMP_API_KEY,
    server: 'us21',
});

/**
 * Test connection to Mailchimp API.
 * @reference https://mailchimp.com/developer/marketing/guides/quick-start/
 */
export async function callPing() {
    console.log('Calling ping...')
    const response = await mailchimp.ping.get();
    console.log(response);
}

/**
 * Add a contact to a list.
 * @param {string} email - Email address of the contact to add
 * @param {string} listId - ID of the list to add the contact to
 * @reference https://mailchimp.com/developer/marketing/guides/create-your-first-audience/
 */
export async function addContactToList(email) {
    const listId = process.env.MAILCHIMP_LIST_ID;
    const response = await mailchimp.lists.addListMember(listId, {
        email_address: email,
        status: 'subscribed'
    });
    console.log(response);
}