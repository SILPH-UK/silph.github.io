const players = [
  { name: "Player 1", Wins: 3 },
  { name: "Player 2", Wins: 5 },
  { name: "Player 3", Wins: 1 }
];
// Function to display the leaderboard
function displayLeaderboard(players) {
  // Sort the players array in descending order based on score
  players.sort((a, b) => b.score - a.score);
  // Print out the leaderboard
  console.log("Leaderboard:");
  players.forEach((player, index) => {
      console.log(`${index + 1}. ${player.name} - ${player.score} points`);
  });
}
displayLeaderboard(players);