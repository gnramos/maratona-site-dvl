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
      'state': {'selectedValues': ['1ªFase']}
    });
}

function pieChartWrapper(containerId, title) {
  return new google.visualization.ChartWrapper({
    chartType: 'PieChart',
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

  malePieChart = pieChartWrapper('male_chart_div', 'Masculina');
  let dashboard = new google.visualization.Dashboard(
      document.getElementById('dashboard_div'));
  dashboard.bind(phasePicker, malePieChart);
  dashboard.draw(male);
}

function drawFemaleDashboard() {
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

function contestIndex() {
  let zero = (thisYear() >= 2022 ? '<li class="list-group"><a href="FaseZero/index.html">Fase Zero</a></li>' : '');
  let summer = `http://maratona.ic.unicamp.br/MaratonaVerao${Number(thisYear()) + 1}`;
  return `<div class="container">
  <div class="row">
    <div class="col-2">
      <a href="Nacional/img/poster_high.png"><img class="img-fluid" src="Nacional/img/poster_low.png"></a>
    </div>
    <div id="male_dashboard_div" class="col-3">
      <div id="male_chart_div"></div>
      <div id="phasePicker_div"></div><br>
    </div>
    <div id="female_dashboard_div" class="col-3">
      <div id="female_chart_div"></div>
    </div>
    <div class="col-4">
      <ul class="list-group">
        ${zero}
        <li class="list-group"><a href="1aFase/index.html">Primeira Fase</a></li>
        <li class="list-group"><a href="Nacional/index.html">Final Nacional</a></li>
        <li class="list-group"><a href="${summer}">Summer School</a></li>
        <li class="list-group"><a href="Mundial/index.html">Final Mundial</a></li>
      </ul>
    </div>
  </div>
</div>`;
}