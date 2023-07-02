import { getCookie } from './helpers.js';
const axios = require('axios');
const mailchimp = require('@mailchimp/mailchimp_marketing');


async function sendRequest(path, data) {
    // Get the CSRF token
    const csrfToken = getCookie('csrftoken');

    // Get root domain
    const domain = window.location.href;

    // combine root domain with path
    const url = domain + path;

    console.log('path:', path);
    console.log('data:', data);
    console.log('domain:', url);

    const params = new URLSearchParams();
    // Convert the data object to a URLSearchParams object
    for (const key in data) {
        params.append(key, data[key]);
    }

    console.log('params:', params.toString());
    console.log('csrfToken:', csrfToken);

    const headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken
    };

    const cookies = {
        'csrftoken': csrfToken
    };

    try {
        const response = await axios.post(url, params.toString(), { headers, withCredentials: true, cookies });
        console.log(response.data); // The response data
    } catch (error) {
        console.error(error);
    }
}


/*
    * Fetch sensitive data from the server.
    * @returns {Promise} - Promise object representing the sensitive data
    * @throws {Error} - Error object
*/
function fetchSensitiveData() {
    return axios.get('/get_sensitive_info/')
        .then(response => response.data)
        .catch(error => {
            console.error('Error fetching sensitive information:', error);
        });
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
    const url = "https://developers.ausha.co/v1/shows/44497/podcasts";
    const tokens = await fetchSensitiveData();

    // Set the headers
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.ausha_api_token}`
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
export async function queryAPIAndCalculateTime() {
    const apiEndpoint = 'https://developers.ausha.co/v1/shows/44497/podcasts';
    const startTime = new Date().getTime(); // Get the current time in milliseconds
    const tokens = await fetchSensitiveData();

    fetch(apiEndpoint, {
        headers: {
            'Authorization': `Bearer ${tokens.ausha_api_token}`
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

export async function callPing() {
    try {
        const tokens = await fetchSensitiveData();
        mailchimp.setConfig({
            apiKey: tokens.mailchimp_api_key,
            server: 'us21',
        });
        console.log('Calling ping...');
        const response = await mailchimp.ping.get();
        console.log(response);
    } catch (error) {
        console.error('An error occurred while calling ping:', error);
    }
}

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
    // // Get the CSRF token with getCookie()
    // const csrftoken = getCookie('csrftoken');

    // console.log('csrftoken:', csrftoken);

    // // Send the request to the server      
    // const formData = new FormData();
    // formData.append('email', email);
    // formData.append('test_status', test_status)

    // try {
    //     const response = await axios.post('/api/proxy/mailchimp/', formData, {
    //         headers: {
    //             'X-CSRFToken': csrftoken,
    //             'Content-Type': 'multipart/form-data'  // Set the content type to form data
    //         }
    //     });
    //     console.log('Response:', response);
    // } catch (error) {
    //     console.error('Error adding contact to list:', error);
    //     throw error;
    // }

    const data = {
        email: email,
        test_status: test_status
    }

    sendRequest('api/proxy/mailchimp/', data)
}