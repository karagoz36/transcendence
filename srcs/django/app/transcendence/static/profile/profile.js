// @ts-check
function udpatePie() {
    const canvas = document.getElementById('statsPieChart');
    if (!canvas) return;
    console.log("canvas=", canvas)

    const existingChart = Chart.getChart(canvas); // Chart.js v3+
    if (existingChart) {
        existingChart.destroy();
    }

    const wins = parseInt(canvas.getAttribute('data-wins'), 10);
    const losses = parseInt(canvas.getAttribute('data-losses'), 10);

    const ctx = canvas.getContext('2d');/*  */
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Wins', 'Losses'],
            datasets: [{
               data: [wins, losses],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.6)',
                    'rgba(220, 53, 69, 0.6)' 
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
                    position: 'bottom',
                }
            }

        }
    });
}

// addEventListener('page-changed', udpatePie);

function main() {
    udpatePie()
}

main()