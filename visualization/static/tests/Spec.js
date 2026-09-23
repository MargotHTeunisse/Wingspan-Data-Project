describe("Distribution chart", () => {
  let container;
  let fetchSpy;

  beforeEach(() => {
    // Like in real template, add a container to set the chart size; keep small for tests.
    container = document.createElement("div")
    container.style.width = "200px"
    container.style.height = "200px"
    container.innerHTML = "<canvas id='chart'></canvas>"
    document.body.appendChild(container)

    // Set a mock API call
    fetchSpy = spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response(JSON.stringify({distribution: {values: [], counts:[]}})))
  )
  });

  afterEach(() => {
    container.remove()
      }
  )

  it("should be a bar chart", async() => {
    await showChart("")

    let chart = Chart.getChart("chart")

    expect(chart.config.type).toEqual("bar")
  });

  it("should have count on y-axis", async() => {
    await showChart("")

    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.y.title.text).toEqual("Count")
    expect(chart.config.options.scales.y.title.display).toEqual(true)
  });

  it("should have property label on x-axis", async() => {
    let label = "Victory points"
    await showChart("", label)

    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.x.title.text).toEqual(label)
    expect(chart.config.options.scales.x.title.display).toEqual(true)
  });

  it("fetches victory points distribution when requested", async() => {
    await showChart("victory_points")

    expect(fetchSpy).toHaveBeenCalledOnceWith('/api/distribution?property=victory_points')
  });

  it("fetches wingspan distribution when requested", async() => {
    await showChart("wingspan")

    expect(fetchSpy).toHaveBeenCalledOnceWith('/api/distribution?property=wingspan')
  });

  it("shows data passed through API", async() => {
    fetchSpy.and.returnValue(
        Promise.resolve(new Response(JSON.stringify({distribution: {values: [4, 5, 6], counts:[3, 2, 1]}})))
    )
    await showChart("")

    let chart = Chart.getChart("chart")

    expect(chart.config.data.labels).toEqual([4, 5, 6])
    expect(chart.config.data.datasets[0].data).toEqual([3, 2, 1])
  });

  it("should have categorical x-axis for qualitative data", async() => {
    fetchSpy.and.returnValue(
        Promise.resolve(
            new Response(JSON.stringify({distribution: {values: ['A', 'B', 'C'], counts:[3, 2, 1]}})))
      )
    await showChart("")
    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.x.type).toEqual('category')
  });

  it("should have linear x-axis for quantitative data", async() => {
    fetchSpy.and.returnValue(
        Promise.resolve(
            new Response(JSON.stringify({distribution: {values: [4, 5, 6], counts:[3, 2, 1]}})))
      )
    await showChart("")
    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.x.type).toEqual('linear')
  })
});
