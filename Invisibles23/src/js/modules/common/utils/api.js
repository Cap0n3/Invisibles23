import { getCookie } from './helpers.js';
const axios = require('axios');

/**
 * Send a request to proxy sever to handle API requests.
 * 
 * @param {string} email - The email address of the contact
 * @param {number} listID - The ID of the list
 * @returns {Promise} - Promise object representing the result of the request
 * @throws {Error} - Error object
 */
async function sendProxyRequest(path, data) {
    // Get the CSRF token
    const csrfToken = getCookie('csrftoken');

    // Get the root domain
    const domain = window.location.origin;

    // Combine root domain with path
    const url = domain + '/' + path;

    const params = new URLSearchParams();
    // Convert the data object to a URLSearchParams object
    for (const key in data) {
        params.append(key, data[key]);
    }

    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
    };

    try {
        const response = await axios.post(url, params.toString(), { headers, withCredentials: true });
        return response.data;
    } catch (error) {
        throw error;
    }
}

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
    const data = {
        show_id: 44497,
    };

    try {
        const allPodcasts = await sendProxyRequest('api/proxy/ausha/', data);
        return (numberOfPodcasts > 0) ? allPodcasts.data.slice(0, numberOfPodcasts) : allPodcasts;
    } catch (error) {
        console.error('Error retrieving podcasts:', error);
        throw error;
    }
}

// ===================== //
// === Mailchimp API === //
// ===================== //

/**
 * Add a contact to the Mailchimp list.
 * 
 * @param {string} email - Email address of the contact
 * @param {int} test_status - For testing, set to any status code to simulate code being returned from the Mailchimp API (default: null)
 * @returns {Promise} - Promise object representing the response from the server
 * @throws {Error} - Error object
 * 
 * @example
 * // Add a contact to the Mailchimp list with await
 * const email = 'test@gmail.com';
 * 
 * try {
 *  const response = await addContactToList(email, test_status);
 * console.log('Response:', response);
 * } catch (error) {
 *  console.error('Error adding contact to list:', error);
 * }
 * 
 * @example
 * // Simulate a http 400 error with test_status
 * const email = 'test@gmail.com'
 * 
 * try {
 *  const response = await addContactToList(email, 400);
 *  console.log('Response:', response);
 * } catch (error) {
 *  console.error('Error adding contact to list:', error);
 * }
 */
export async function addContactToList(email, test_status = null) {
    const data = {
        email: email,
        test_status: test_status
    }

    try {
        const response = await sendProxyRequest('api/proxy/mailchimp/', data);
        console.log('API response: ', response);
    }
    catch (error) {
        console.error('Error adding contact to list:', error);
        throw error;
    }
}