describe("Distribution chart", () => {
  let container;

  beforeEach(() => {
    // Like in real template, add a container to set the chart size; keep small for tests.
    container = document.createElement("div")
    container.style.width = "200px"
    container.style.height = "200px"
    container.innerHTML = "<canvas id='chart'></canvas>"
    document.body.appendChild(container)
  });

  afterEach(() => {
    container.remove()
      }
  )

  it("should be a bar chart", () => {
    showChart("")

    let chart = Chart.getChart("chart")

    expect(chart.config.type).toEqual("bar")
  });
})
