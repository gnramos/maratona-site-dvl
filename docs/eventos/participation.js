google.charts.load('current', {'packages':['corechart', 'controls']});
google.charts.setOnLoadCallback(drawMaleDashboard);
google.charts.setOnLoadCallback(drawFemaleDashboard);

let phasePicker = undefined;
let malePieChart = undefined;
let femalePieChart = undefined;

/**
 * Returns a control wrapper object for filtering results by phase.
 *
 * @return {ControlWrapper} the wrapper object
 */
function phasePickerWrapper() {
  return new google.visualization.ControlWrapper({
      'controlType': 'CategoryFilter',
      'containerId': 'phasePicker_div',
      'options': {
        'filterColumnIndex': 0,
        'ui': {
          'sortValues': false,
          'label': 'Filtro:',
          'allowTyping': false,
          'allowMultiple': false,
          'allowNone': false
        }
      },
      'state': {'selectedValues': [CONFIG.phases[0].name]}
    });
}

/**
 * Returns a pie chart object.
 *
 * @return {ControlWrapper} the wrapper object
 */
function pieChartWrapper(containerId, title) {
  return new google.visualization.ChartWrapper({
    'chartType': 'PieChart',
    'containerId': containerId,
    'options': {
      'legend': 'none',
      'pieSliceText': 'label',
      'title': `Participação ${title}`
    },
    'view': {'columns': [1, 2]}
  });
}

/**
 * Draws the pie chart for male participation results.
 */
function drawMaleDashboard() {
  if (phasePicker === undefined)
    phasePicker = phasePickerWrapper();
    male.unshift(['Phase', 'Region', 'Participants']);
    female.unshift(['Phase', 'Region', 'Participants']);

  malePieChart = pieChartWrapper('male_chart_div', 'Masculina');
  let dashboard = new google.visualization.Dashboard(
      document.getElementById('dashboard_div'));
  dashboard.bind(phasePicker, malePieChart);
  dashboard.draw(male);
}

/**
 * Draws the pie chart for female participation results.
 *
 * Binds the results to the phasePicker object.
 */
function drawFemaleDashboard(){
  femalePieChart = pieChartWrapper('female_chart_div', 'Feminina');
  google.visualization.events.addListener(malePieChart, 'ready', function () {
    let data = google.visualization.arrayToDataTable(female);
    let view = new google.visualization.DataView(data);
    let phase = phasePicker.getState().selectedValues[0];
    view.setRows(data.getFilteredRows([{column: 0, value: phase}]));
    femalePieChart.setDataTable(view);
    femalePieChart.draw();
    });
}

/**
 * Builds the page body for an event.
 *
 * There are 3 parts: the folder, the pie chars with contestant statistics, and
 * the links for each phase's HTML page.
 *
 * @return {String} the HTML with the formatted information
 */
function eventPageBody() {
  function phaseList(year) {
    let items = '';
    for (phase of CONFIG.phases) {
      if (year >= phase.start)
        items += `\n<li><a href="${phase.dir}/index.html">${phase.name}</a></li>`;
        if (phase.name == 'Nacional' && year >= 2012 && year != 2021)
          items += `\n<li><a href="http://maratona.ic.unicamp.br/MaratonaVerao${Number(year) + 1}">Summer School</a></li>`;
    }
    return `<ul class="list-group">
  <li class="list-group"><strong>Informações:</strong></li>
  ${items}
</ul>`;
  }

  let url = window.location.pathname.split('/');
  let year = (isNaN(parseInt(url.at(-3))) ? url.at(-2) : url.at(-3));
  let header = bodyHeader(fullName(year, ` (${year})`), makeBreadcrumbs());

  return `${header}
<div class="container">
  <div class="row">
    <div class="col-2 d-flex align-items-center">
      <a href="Nacional/img/poster_high.png"><img class="img-fluid" src="Nacional/img/poster_low.png" onerror="this.src='../../img/maratona-logo.jpg'"></a>
    </div>
    <div id="male_dashboard_div" class="col-3">
      <div id="male_chart_div"></div>
      <div id="phasePicker_div"></div><br>
    </div>
    <div id="female_dashboard_div" class="col-3">
      <div id="female_chart_div"></div>
    </div>
    <div class="col-4 d-flex align-items-center">
      ${phaseList(year)}
    </div>
  </div>
</div>
${bodyFooter()}`;
}

/**
 * Return the year for specific events from the dir structure.
 *
 * @return {String} the year.
 */
function thisYear() {
  let url = window.location.pathname.split('/');
  return (isNaN(parseInt(url.at(-3))) ? url.at(-2) : url.at(-3));
}