
function loadStats() {
    $.getJSON("/stats", function (data) {
        createBarChart('chart-frequent', 'Jogos que a dezena apareceu', data.most_frequent.map(x => x[0]), data.most_frequent.map(x => x[1]));
        createBarChart('chart-missing', 'Há quantos jogos a dezena não aparece', data.longest_missing.map(x => x[0]), data.longest_missing.map(x => x[1]));

        var oddData = data.odd_even.odd;
        var allEvens = data.odd_even.even.find(x => x[0] === 6);
        if (allEvens) {
            oddData.push([0, allEvens[1]]);
        }
        oddData.sort((a, b) => a[0] - b[0]);
        createBarChart('chart-odd-even', 'Frequência', oddData.map(x => x[0]), oddData.map(x => x[1]));
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
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

$(document).ready(function () {
    loadStats();
});
