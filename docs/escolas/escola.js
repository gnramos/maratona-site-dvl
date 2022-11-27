const RESULT_LEN = 5;

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
  function rankImg(year, phase, heightPx, rank, reverse=false) {
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

    if (reverse)
      images = images.slice().reverse();

    for (let img of images)
      imgHTML += ` <img src="${root()}img/${img}.png" style="height:${heightPx}px; width: auto;"> `;

    return imgHTML;
  }
  function toolTip(year, phase, rank) {
    return `<div style="padding:5px 5px 5px 5px; min-width:75px;"><strong>Rank:</strong> ${rank} ${rankImg(year, phase, 12, rank)}</div>`;
  }

  rows = rows.slice(-RESULT_LEN);

  google.charts.load('current', {packages: ['corechart', 'line']});
  let data = new google.visualization.DataTable();
  data.addColumn('string', 'Year');
  for (let phase of ['1aFase', 'Nacional', 'Mundial']) {
    data.addColumn('number', phase);
    data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
  }
  for (let row of rows)
    data.addRow([row[0], // year
                 row[1], toolTip(row[0], '1aFase', row[1] == null ? '' : row[1]),
                 row[2], toolTip(row[0], 'Nacional', row[2] == null ? '': row[2]),
                 row[3], toolTip(row[0], 'Mundial', row[3] == null ? '': row[3])]);

  let options = {hAxis: {title: 'Ano'},
                 vAxis: {title: 'Rank', baseline: 1, direction: -1},
                 legend: {position: 'top'},
                 tooltip: {isHtml: true}};

  let lineChart = new google.visualization.LineChart(chart);
  lineChart.draw(data, options);
}

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