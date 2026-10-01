async function showChart() {
    let select_menu = document.getElementById("1D_plot_property_selection")
    let property = select_menu.value
    let label = select_menu.options[select_menu.selectedIndex].text

    let context = document.getElementById("chart")

    let chart = Chart.getChart("chart")
    if (chart !== undefined) {
        chart.destroy()
    }

    let distribution = {values:null, counts:null}
    let bird_data
    if (document.getElementById("search_only").checked) {
        bird_data = JSON.parse(document.getElementById("search_results_json").text)
    }
    else {
        bird_data = await fetch('/api/all-birds')
            .then(response => response.json())
    }

    let property_data = {}
    for (let index in bird_data) {
        let val = bird_data[index][property]
        if (val === undefined) {
            throw("Property is undefined for one or more birds.")
        }
        property_data[val] = property_data[val]? property_data[val] + 1 : 1
    }

    distribution.values = Object.keys(property_data)
    distribution.counts = Object.values(property_data)

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