describe("Distribution chart", () => {
  let container;
  let select_menu;
  let search_only_toggle;
  let search_results_json;
  let fetchSpy;

  let test_data = [
          {'scientific_name': 'Limosa limosa', 'victory_points': 6, 'wingspan':76, 'nest_type':'GRND'},
          {'scientific_name': 'Falco subbuteo', 'victory_points': 4, 'wingspan':75, 'nest_type':'PLTF'},
          {'scientific_name': 'Falco peregrinus', 'victory_points': 5, 'wingspan':104, 'nest_type':'PLTF'},
          {'scientific_name': 'Accipiter gentilis', 'victory_points': 5, 'wingspan':106, 'nest_type':'PLTF'}
        ]

  let test_search_data = [
          {'scientific_name': 'Falco subbuteo', 'victory_points': 4, 'wingspan':75, 'nest_type':'PLTF'},
          {'scientific_name': 'Falco peregrinus', 'victory_points': 5, 'wingspan':104, 'nest_type':'PLTF'},
        ]

  beforeEach(() => {
    // Like in real template, add a container to set the chart size; keep small for tests.
    container = document.createElement("div")
    container.style.width = "200px"
    container.style.height = "200px"
    container.innerHTML = "<canvas id='chart'></canvas>"
    document.body.appendChild(container)

    select_menu = document.createElement("select")
    select_menu.id = "1D_plot_property_selection"
    let option = document.createElement("option")
    option.value = "victory_points"
    option.text = "Victory points"
    select_menu.appendChild(option)
    document.body.appendChild(select_menu)

    search_only_toggle = document.createElement("input")
    search_only_toggle.id = "search_only"
    search_only_toggle.type = "checkbox"
    document.body.appendChild(search_only_toggle)

    search_results_json = document.createElement("script")
    search_results_json.id = "search_results_json"
    search_results_json.text = JSON.stringify(test_search_data)
    document.body.appendChild(search_results_json)

    // Set a mock API call using test data
    fetchSpy = spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response(JSON.stringify(test_data)))
  )
  });

  afterEach(() => {
    container.remove()
    search_only_toggle.remove()
    select_menu.remove()
    search_results_json.remove()
    }
  )

  it("should be a bar chart", async() => {
    await showChart()

    let chart = Chart.getChart("chart")

    expect(chart.config.type).toEqual("bar")
  });

  it("should have count on y-axis", async() => {
    await showChart()

    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.y.title.text).toEqual("Count")
    expect(chart.config.options.scales.y.title.display).toEqual(true)
  });

  it("should have property label on x-axis", async() => {
    await showChart()

    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.x.title.text).toEqual("Victory points")
    expect(chart.config.options.scales.x.title.display).toEqual(true)
  });

  it("fetches all birds when search-only mode is not toggled", async() => {
    await showChart()

    expect(fetchSpy).toHaveBeenCalledOnceWith('/api/all-birds')
  });

  it("does not call API when search-only mode is toggled", async() => {
    search_only_toggle.click()

    await showChart()

    expect(fetchSpy).toHaveBeenCalledTimes(0)
  })

  it("shows victory points data from API when search-only is not toggled", async() => {
    await showChart()

    let chart = Chart.getChart("chart")

    expect(chart.config.data.labels).toEqual(['4', '5', '6'])
    expect(chart.config.data.datasets[0].data).toEqual([1, 2, 1])
  })

  it("shows victory points data from DOM when search-only is toggled", async() => {
    search_only_toggle.click()

    await showChart()

    let chart = Chart.getChart("chart")

    expect(chart.config.data.labels).toEqual(['4', '5'])
    expect(chart.config.data.datasets[0].data).toEqual([1, 1])
  })

  it("shows wingspan data passed from API when search-only is not toggled", async() => {
    let option = document.createElement("option")
    option.value = "wingspan"
    option.selected = true
    select_menu.appendChild(option)

    await showChart()

      let chart = Chart.getChart("chart")

      expect(chart.config.data.labels).toEqual(['75', '76', '104', '106'])
    expect(chart.config.data.datasets[0].data).toEqual([1, 1, 1, 1])
  });

  it("should have categorical x-axis for qualitative data", async() => {
    let option = document.createElement("option")
    option.value = "nest_type"
    option.selected = true
    select_menu.appendChild(option)

    await showChart()
    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.x.type).toEqual('category')
  });

  it("should have linear x-axis for quantitative data", async() => {
    await showChart()
    let chart = Chart.getChart("chart")

    expect(chart.config.options.scales.x.type).toEqual('linear')
  })
});
