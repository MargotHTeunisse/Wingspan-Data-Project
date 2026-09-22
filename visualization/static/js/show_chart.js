async function showChart(property, label) {
    let context = document.getElementById("chart")

    await fetch('/api/distribution/'+property).then(response => response.json())

    let chart = Chart.getChart("chart")
    if (chart !== undefined) {
        chart.destroy()
    }

    const newChart = new Chart(context,
        {
            type: "bar",
            data: {
                labels: ['A', 'B', 'C'],
                datasets: [{
                    data: [1, 3, 2],
                }]
            },
            options: {
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: "Count"
                        }
                    },

                    x: {
                        title: {
                            display: true,
                            text: label
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                 legend: {
                    display: false
                 }
                }
            }
        })
    context.style.backgroundColor="#FFFFFF"

    newChart.update('show')
}