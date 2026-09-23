async function showChart(property, label) {
    let context = document.getElementById("chart")

    let distribution = await fetch('/api/distribution/'+property)
        .then(response => response.json())
        .then(response => response.distribution)

    let chart = Chart.getChart("chart")
    if (chart !== undefined) {
        chart.destroy()
    }

    const newChart = new Chart(context,
        {
            type: "bar",
            data: {
                labels: distribution.values,
                datasets: [{
                    data: distribution.counts,
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