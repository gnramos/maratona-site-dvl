/**
 * Draw a graphic with the results.
 *
 * Assumes the results are ordered and that each result is in the following format:
 * [year, phases].
 *
 * @param  {Array}  rows  the results
 */
function drawHistory(results, chartId='chart_div', controlId='control_div') {
  function rankImg(year, phase, heightPx, rank) {
    let multiplier = 4, images = [], imgHTML = "";

    if (phase == '1ªFase')
      multiplier = 1;
    if (phase == 'Nacional' && year < 2021)
      multiplier = 3;

    if (rank <= 1 * multiplier)
      images.push("gold_medal");
    else if (rank <= 2 * multiplier)
      images.push("silver_medal");
    else if (rank <= 3 * multiplier)
      images.push("bronze_medal");

    if (phase == "Nacional" && rank == 1)
      images.push("trophy");

    for (let img of images)
      imgHTML += ` <img src="${root()}img/${img}.png" style="height:${heightPx}px; width: auto;"> `;

    return imgHTML;
  }

  function toolTip(year, phase, rank) {
    return `<div style="padding:5px 5px 5px 5px; min-width:75px;"><strong>Rank:</strong> ${rank} ${rankImg(year, phase, 12, rank)}</div>`;
  }

  function dataTable(results) {
    let data = new google.visualization.DataTable();
    data.addColumn('number', 'Year');
    for (let phase of CONFIG.phases) {
      data.addColumn('number', phase.name);
      data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
    }

    for (let row of results) {
      let thisRow = [parseInt(row[0])];
      for (let i in CONFIG.phases) {
        i = Number(i) + 1;
        thisRow.push(row[i]);
        thisRow.push(toolTip(row[0], CONFIG.phases[i - 1].name, row[i] == null ? '' : row[i]));
      }
      data.addRow(thisRow);
    }

    return data;
  }

  google.charts.load('current', {packages: ['corechart', 'controls']});

  let data = dataTable(results);
  data.removeColumn(1); // Fase 0
  let lastYear = parseInt(results.slice(-1)[0][0]);
  let firstYear = Math.max(parseInt(results[0][0]), lastYear - CONFIG.schools.chart.show_last_years + 1);
  let chartWrapper = new google.visualization.ChartWrapper({
    'chartType': 'LineChart',
    'containerId': chartId,
    'options': {hAxis: {title: 'Ano', format: '0'},
                vAxis: {title: 'Rank', format: '0', baseline: 1, direction: -1},
                legend: {position: 'top'},
                pointSize: 10,
                tooltip: {isHtml: true}
               }
  })

  let control = new google.visualization.ControlWrapper({
    'controlType': 'ChartRangeFilter',
    'containerId': controlId,
    'options': {
                filterColumnLabel: 'Year',
                minRangeSize: 1,
                ui: {chartOptions: { hAxis: {format: '0'},
                                     vAxis: {format: '0', direction: -1}}}
            },
    state: {
            range: {start: firstYear,
                    end: lastYear}},
  });

  let dashboard = new google.visualization.Dashboard(
      document.getElementById('dashboard_div'));
  dashboard.bind([control], [chartWrapper]);
  dashboard.draw(data);

  google.visualization.events.addListener(chartWrapper, 'select', function(e) {
    let selection = dashboard.getSelection()[0];
    let year = results[selection['row']][0], //
       phase = CONFIG.phases[selection['column'] / 2].dir; // /2 para lidar com a tooltip
    window.location = `../../../historico/${year}/${phase}/index.html`;
  });
}

/**
 * Builds breadcrumbs for given items.
 *
 * @param  {Array}  items Array of items
 * @return {String}       the HTML with the formatted information
 */
function makeBreadcrumbs(items) {
  let bcItems = '';
  for (item of items)
    bcItems += `\n<li class="breadcrumb-item">${item}</li>`
  return `
<nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb">
  <ol class="breadcrumb">
    ${bcItems}
  </ol>
</nav>`
}