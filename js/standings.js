// URL of the CSV file
const csvUrl = 'https://wipedout36.github.io/standings.csv">'; // Replace with your CSV URL

// Parse CSV function
function parseCSV(data) {
    const rows = data.split('\n').map(row => row.split(','));
    const headers = rows.shift();
    return rows.map(row => Object.fromEntries(headers.map((header, i) => [header.trim(), row[i]?.trim() || ''])));
}

// Process data to create leaderboard
function generateLeaderboard(data) {
    return data.map(row => ({
        player: row['Player'],
        wins: parseInt(row['Wins'], 10) || 0,
        losses: parseInt(row['Losses'], 10) || 0,
        draws: parseInt(row['Draws'], 10) || 0
    }));
}

// Render leaderboard as a table
function renderLeaderboard(leaderboard) {
    const container = document.getElementById('leaderboard-container');
    const table = document.createElement('table');

    // Create table header
    const headerRow = document.createElement('tr');
    ['Player', 'Wins', 'Losses', 'Draws', 'Total Points'].forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Populate table rows
    leaderboard.forEach(({ player, wins, losses, draws }) => {
        const tr = document.createElement('tr');
        const totalPoints = wins * 3 + draws; // Example point calculation
        [player, wins, losses, draws, totalPoints].forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });

    container.innerHTML = '';
    container.appendChild(table);
}

// Main function to fetch and display leaderboard
async function displayLeaderboard() {
    try {
        const response = await fetch(csvUrl);
        if (!response.ok) throw new Error('Failed to fetch CSV');
        const csvText = await response.text();
        const parsedData = parseCSV(csvText);
        const leaderboard = generateLeaderboard(parsedData);
        renderLeaderboard(leaderboard);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('leaderboard-container').textContent = 'Failed to load leaderboard.';
    }
}

// Slideshow logic
function startSlideshow() {
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('hidden', i !== index);
        });
    }

    setInterval(() => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }, 5000); // Change every 5 seconds

    showSlide(currentSlide); // Show the first slide initially
}

// Initialize app
displayLeaderboard();
startSlideshow();