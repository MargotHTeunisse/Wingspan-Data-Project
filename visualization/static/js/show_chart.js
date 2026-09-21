function showChart(property) {
    let context = document.getElementById("chart")

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
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                title: {
                    display: true,
                    text: property
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