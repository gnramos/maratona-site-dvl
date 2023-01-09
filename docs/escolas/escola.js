const YEARS_TO_SHOW = 5;

/**
 * Draw a graphic with the results.
 *
 * Assumes the results are ordered and that each result is in the following format:
 * [year, PHASES]. Always shows the last RESULT_LEN values.
 *
 * @param  {Array}  rows  the results
 */
function drawHistory(rows) {
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

  function dataTable(rows) {
    let data = new google.visualization.DataTable();
    data.addColumn('number', 'Year');
    for (let phase of PHASES) {
      data.addColumn('number', phase);
      data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
    }

    for (let row of rows) {
      let thisRow = [parseInt(row[0])];
      for (let phase in PHASES) {
        phase = Number(phase) + 1;
        thisRow.push(row[phase]);
        thisRow.push(toolTip(row[0], PHASES[phase - 1], row[phase] == null ? '' : row[phase]));
      }
      data.addRow(thisRow);
    }

    return data;
  }

  google.charts.load('current', {packages: ['corechart', 'controls']});

  // let data = dataTable(rows.slice(-YEARS_TO_SHOW));
  // let lineChart = new google.visualization.LineChart(chart_div);
  // lineChart.draw(data, {hAxis: {title: 'Ano', format: '0'},
  //                       vAxis: {title: 'Rank', baseline: 1, direction: -1, format: '0'},
  //                       legend: {position: 'top'},
  //                       pointSize: 10,
  //                       tooltip: {isHtml: true}});

  let data = dataTable(rows);
  data.removeColumn(1); // Fase 0
  let lastYear = parseInt(rows.slice(-1)[0][0]);
  let firstYear = parseInt(rows[0][0]);
  if (firstYear < lastYear - YEARS_TO_SHOW + 1)
    firstYear = lastYear - YEARS_TO_SHOW + 1;
  let chart = new google.visualization.ChartWrapper({
    chartType: 'LineChart',
    containerId: 'chart_div',
    options: {hAxis: {title: 'Ano', format: '0'},
              vAxis: {title: 'Rank', format: '0', baseline: 1, direction: -1},
              legend: {position: 'top'},
              pointSize: 10,
              tooltip: {isHtml: true}
            }
  })

  let control = new google.visualization.ControlWrapper({
    controlType: 'ChartRangeFilter',
    containerId: 'control_div',
    options: {
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
  dashboard.bind([control], [chart]);
  dashboard.draw(data);

  google.visualization.events.addListener(chart, 'select', function(e) {
    let selection = chart.getChart().getSelection()[0];
    let year = results[selection['row']][0],
       phase = PHASE_DIR[selection['column'] / 2]; // /2 para lidar com a tooltip
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