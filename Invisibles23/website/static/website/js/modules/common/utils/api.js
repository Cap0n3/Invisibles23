// api.js
export async function getLastPodcasts() {
    // construct URL
    const url = new URL('https://642eb6132b883abc6414f220.mockapi.io/episodes');
    url.searchParams.append('limit', 1);

    try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // return data;
        console.log(data)
    } 
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}


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