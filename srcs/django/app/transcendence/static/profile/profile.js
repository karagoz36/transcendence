// @ts-check
function udpatePie() {
    console.log("test")
    const canvas = document.getElementById('statsPieChart');

    // Requête pour récupérer les stats
    const wins = parseInt(canvas.getAttribute('data-wins'), 10);
    const losses = parseInt(canvas.getAttribute('data-losses'), 10);

    console.log(wins)
    console.log(losses)
    // Initialisation du graphique
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'pie', // Diagramme circulaire
        data: {
            labels: ['Wins', 'Losses'],
            datasets: [{
               data: [wins, losses],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.6)', // Vert pour les "Wins"
                    'rgba(220, 53, 69, 0.6)'  // Rouge pour les "Losses"
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom', // Légende sous le graphique
                }
            }

        }
    });
}

addEventListener('page-changed', udpatePie);
document.addEventListener("DOMContentLoaded", udpatePie)