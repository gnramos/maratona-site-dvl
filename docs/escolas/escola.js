const RESULT_LEN = 5;
const PHASES = ['1aFase', 'Nacional', /* 'Programadores', */ 'Mundial'];

/**
 * Draw a graphic with the results.
 *
 * Assumes the results are ordered and that each result is in the following format:
 * [year, rank1stPhase, rankNationalFinals, rankWorldFinals]. Always shows the last
 * RESULT_LEN values.
 *
 * @param  {Array}  rows  the results
 */
function drawVisualization(rows) {
  function rankImg(year, phase, heightPx, rank) {
    let multiplier = (phase == "Nacional") ? (year > 2020 ? 4 : 3) : 1,
    images = [], imgHTML = "";

    if (rank > 0)
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
    data.addColumn('string', 'Year');
    for (let phase of PHASES) {
      data.addColumn('number', phase);
      data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
    }

    for (let row of rows) {
      let thisRow = [row[0]];
      for (let phase in PHASES) {
        phase = Number(phase) + 1;
        thisRow.push(row[phase]);
        thisRow.push(toolTip(row[0], PHASES[phase - 1], row[phase] == null ? '' : row[phase]));
      }
      data.addRow(thisRow);
    }

    return data;
  }

  google.charts.load('current', {packages: ['corechart', 'line']});

  let options = {hAxis: {title: 'Ano'},
                 vAxis: {title: 'Rank', baseline: 1, direction: -1},
                 legend: {position: 'top'},
                 pointSize: 10,
                 tooltip: {isHtml: true}};

  let lineChart = new google.visualization.LineChart(chart);
  lineChart.draw(dataTable(rows.slice(-RESULT_LEN)), options);
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