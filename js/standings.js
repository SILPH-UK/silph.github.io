// leaderboard.js

const sheetUrl = 'https://spreadsheets.google.com/feeds/list/2PACX-1vSg2Mykla0mZRlCUP_ta-BNq29EN9qzoNoYI8fme6Yx5r3j_PPJqO0ikv3nYB7UZki0O7SP_TA_jJCB/1/public/full?alt=json'

async function fetchLeaderboardData() {
    try {
        // Fetch data from Google Sheets
        const response = await fetch(sheetUrl);
        const data = await response.json();

        // Parse the relevant data into an array
        const players = data.feed.entry.map(entry => ({
            Name: entry.gsx$Name.$t,   // Adjust the column names as per your Google Sheets headers
            Wins: parseInt(entry.gsx$Wins.$t) // Assuming 'score' is numeric
        }));

        // Sort the players array by score (descending)
        players.sort((a, b) => b.Wins - a.Wins);

        // Display the leaderboard in the HTML
        const leaderboardDiv = document.getElementById("slideshow-container");
        leaderboardDiv.innerHTML = ""; // Clear any previous content

        players.forEach((player, index) => {
            const playerElement = document.createElement("p");
            playerElement.textContent = `${index + 1}. ${player.Wins} - ${player.Wins} points`;
            leaderboardDiv.appendChild(playerElement);
        });

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Call the function to fetch data and display the leaderboard
fetchLeaderboardData();
