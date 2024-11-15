// leaderboard.js

// Sample data: an array of players with their names and scores
const players = [
    { name: "Player 1", score: 1 },
    { name: "Player 2", score: 2 },
    { name: "Player 3", score: 3 }
];

// Function to display the leaderboard
function displayLeaderboard(players) {
    // Sort the players array in descending order based on score
    players.sort((a, b) => b.score - a.score);

    // Get the leaderboard div element
    const leaderboardDiv = document.getElementById("slideshow-container");
    leaderboardDiv.innerHTML = ""; // Clear any previous content

    // Create leaderboard items and display them
    players.forEach((player, index) => {
        const playerElement = document.createElement("p");
        playerElement.textContent = `${index + 1}. ${player.name} - ${player.score} points`;
        leaderboardDiv.appendChild(playerElement);
    });
}

// Call the function to display the leaderboard
displayLeaderboard(players);
