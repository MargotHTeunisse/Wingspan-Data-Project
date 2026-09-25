async function showChart() {
    let select_menu = document.getElementById("1D_plot_property_selection")
    let property = select_menu.value
    let label = select_menu.options[select_menu.selectedIndex].text

    let context = document.getElementById("chart")

    let chart = Chart.getChart("chart")
    if (chart !== undefined) {
        chart.destroy()
    }

    let distribution = {values: null, counts: null}
    if (document.getElementById("search_only").checked) {
        distribution.values = []
        distribution.counts = []
    }
    else {
    distribution = await fetch('/api/distribution?property=' + property)
            .then(response => response.json())
            .then(response => response.distribution)
    }

    let dataIsNumerical = Object.values(distribution.values).every(val => isFinite(val))

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
                animation: {
                    duration: 500
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: "Count"
                        }
                    },

                    x: {
                        type: dataIsNumerical? 'linear':'category',
                        title: {
                            display: true,
                            text: label
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: false,
                        text: "Property distribution (" + distribution.counts.reduce((a, b) => a+b, 0)
                            + " birds)"
                    },
                 legend: {
                    display: false
                 }
                }
            }
        })
    context.style.backgroundColor="#FFFFFF"

    newChart.update('show')
}