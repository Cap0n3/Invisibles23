// api.js
const axios = require('axios');

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

// Usage example
// const n = 5; // Get the last 5 podcasts
// getLastNPodcasts(n)
//     .then(podcasts => {
//         console.log('Last', n, 'podcasts:', podcasts);
//         // Do something with the podcasts
//     })
//     .catch(error => {
//         // Handle the error
//         console.error('Error retrieving podcasts:', error);
//     });




// export async function getLastPodcasts() {
//     // construct URL
//     const url = new URL('https://642eb6132b883abc6414f220.mockapi.io/episodes');
//     url.searchParams.append('limit', 1);

//     try {
//         const response = await fetch(url);
//         if (!response.ok) {
//           throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const data = await response.json();
//         // return data;
//         console.log(data)
//     } 
//     catch (error) {
//         console.error('There was a problem with the fetch operation:', error);
//     }
// }


// function loadEpisodes() {
//     console.log("LOADED !!!");
//     const url = new URL('https://642eb6132b883abc6414f220.mockapi.io/episodes');
//     url.searchParams.append('limit', 1);
    
//     fetch(url, {
//       method: 'GET',
//       headers: {'content-type':'application/json'},
//     }).then(res => {
//       if (res.ok) {
//           return res.json();
//       }
//       // handle error
//     }).then(tasks => {
//         console.log("LOADED !!!")
//       // mockapi returns first 10 tasks that are not completed
//     }).catch(error => {
//       // handle error
//     })
// }