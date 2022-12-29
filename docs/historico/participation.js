google.charts.load('current', {'packages':['corechart', 'controls']});
google.charts.setOnLoadCallback(drawMaleDashboard);
google.charts.setOnLoadCallback(drawFemaleDashboard);

let phasePicker = undefined;
let malePieChart = undefined;
let femalePieChart = undefined;

function createPhasePicker() {
  return new google.visualization.ControlWrapper({
      'controlType': 'CategoryFilter',
      'containerId': 'phasePicker_div',
      'options': {
        'filterColumnIndex': 0,
        'ui': {
          'sortValues': false,
          'label': 'Fase:',
          'allowTyping': false,
          'allowMultiple': false,
          'allowNone': false
        }
      },
      'state': {'selectedValues': [PHASES[0]]}
    });
}

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

function drawMaleDashboard() {
  if (phasePicker === undefined)
    phasePicker = createPhasePicker();
    male.unshift(['Phase', 'Region', 'Participants']);
    female.unshift(['Phase', 'Region', 'Participants']);

  malePieChart = pieChartWrapper('male_chart_div', 'Masculina');
  let dashboard = new google.visualization.Dashboard(
      document.getElementById('dashboard_div'));
  dashboard.bind(phasePicker, malePieChart);
  dashboard.draw(male);
}

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

function phaseItems() {
  let links = '';
  if (thisYear() >= 2022)
    links += '\n<li><a href="Zero/index.html">Fase 0</a></li>'
  if (thisYear() >= 2004)
    links += '\n<li><a href="Primeira/index.html">Primeira Fase</a></li>';
  links += '\n<li><a href="Nacional/index.html">Final Nacional</a></li>';
  if (thisYear() >= 2012 && thisYear() != 2021)
    links += `\n<li><a href="http://maratona.ic.unicamp.br/MaratonaVerao${Number(thisYear()) + 1}">Summer School</a></li>`;
  links += '\n<li><a href="Mundial/index.html">Final Mundial</a></li>';
  return links;
}

function contestIndex(primeira=true) {
  let header = bodyHeader(`${toRoman(thisYear() - 1995)} Maratona SBC de Programação (${thisYear()})`, makeBreadcrumbs());
  return `${header}
<div class="container">
  <div class="row">
    <div class="col-2">
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
      <ul class="list-group">
        <li class="list-group"><strong>Informações:</strong></li>
        ${phaseItems(primeira)}
      </ul>
    </div>
  </div>
</div>
${bodyFooter()}`;
}