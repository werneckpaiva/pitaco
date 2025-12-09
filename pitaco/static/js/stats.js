
var gapChartInstance = null;
var cachedGapData = null;


function loadStats() {
    $.getJSON("/stats", function (data) {
        createBarChart('chart-frequent', 'Jogos que a dezena apareceu', data.most_frequent.map(x => x[0]), data.most_frequent.map(x => x[1]));
        createBarChart('chart-missing', 'Há quantos jogos a dezena não aparece', data.longest_missing.map(x => x[0]), data.longest_missing.map(x => x[1]));

        var gapData = data.gap_distribution;

        // 1. Identify all unique X-axis labels (gap sizes)
        var allLabels = new Set();
        gapData.forEach(dist => dist.forEach(item => allLabels.add(item[0])));
        var labels = Array.from(allLabels).sort((a, b) => a - b);

        // 2. Build datasets
        var datasets = [];
        var colors = [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 206, 86)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)'
        ];

        for (var i = 0; i < 5; i++) {
            var distMap = new Map(gapData[i]);
            // Map common labels to this gap's data, filling 0 where missing
            var dataPoints = labels.map(l => distMap.get(l) || 0);

            datasets.push({
                label: (i + 1) + 'º Gap',
                data: dataPoints,
                borderColor: colors[i],
                backgroundColor: colors[i],
                borderWidth: 2,
                fill: false,
                tension: 0.1,
                pointRadius: 2
            });
        }

        createLineChart('chart-gap', labels, datasets);
    });
}

function createLineChart(canvasId, labels, datasets) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(3);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Probabilidade'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Tamanho da Distância (Gap)'
                    }
                }
            }
        }
    });
}

function createBarChart(canvasId, label, labels, data) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(24, 188, 156, 0.6)',
                borderColor: 'rgba(24, 188, 156, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

$(document).ready(function () {
    loadStats();
});
