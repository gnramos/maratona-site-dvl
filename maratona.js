CURRENT_YEAR = 2022;

function contact(text, ...args) {
    var mail = args.reduce((acc, cur) => acc + cur);
    return `<a href="mailto:${mail}">${text}</a>`;
}

function root() {
  var url = window.location.pathname.split('/');
  return '../'.repeat(url.length - 3);
  // return '../'.repeat(url.length - 8);
}

function header() {
  var url = window.location.pathname.split('/');
  var currentPage = url.at(-1), currentDir = url.at(-2);
  if (!currentPage.endsWith('html'))
    currentPage = 'index.html';
  var selected = `class="nav-link active" aria-current="page"`,
      unselected = `class="nav-link"`;

  document.write(`
    <div class="container">
      <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
        <a href="${root()}index.html" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
          <img src="${root()}img/maratona-logo.jpg" class="bi me-2" height="32">
          <span class="fs-4">Maratona de Programação</span>
        </a>
        <ul class="nav nav-pills">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle ${currentDir == 'sobre' ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Sobre
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="${root()}sobre/index.html">O que é?</a></li>
              <li><a class="dropdown-item" href="${root()}sobre/regras.html">Regras</a></li>
              <li><a class="dropdown-item" href="${root()}sobre/ambiente_computacional.html">Ambiente Computacional</a></li>
              <li><a class="dropdown-item" href="${root()}sobre/organizacao.html">Organização</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle ${currentDir == CURRENT_YEAR ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Participe!
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="${root()}inscricoes.html">Inscrições</a></li>
              <li><a class="dropdown-item" href="${root()}historico/${CURRENT_YEAR}/FaseZero.html">Fase Zero</a></li>
              <li><a class="dropdown-item" href="${root()}historico/${CURRENT_YEAR}/1aFase.html">Primeira Fase</a></li>
              <li><a class="dropdown-item" href="${root()}historico/${CURRENT_YEAR}/Nacional.html">Final Nacional</a></li>
              <li><a class="dropdown-item" href="${root()}historico/${CURRENT_YEAR}/SummerSchool.html">Summer School</a></li>
              <li><a class="dropdown-item" href="${root()}historico/${CURRENT_YEAR}/Mundial.html">Final Mundial</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle ${['historico', 'instituticoes'].includes(currentDir) ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Informações
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="${root()}historico/index.html">Competições Passadas</a></li>
              <li><a class="dropdown-item" href="https://gnramos.github.io/maratona-site">Estatísticas</a></li>
              <li><a class="dropdown-item" href="${root()}instituicoes/index.html">Instituições</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a href="${root()}contato.html" ${currentPage == 'contato.html' ? selected : unselected}>Contato</a>
          </li>
          <li class="nav-item">
            <a href="https://www.facebook.com/maratona/" class="nav-link">
              <i class="bi bi-facebook" fill="currentColor">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                  <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
                </svg>
              </i>
            </a>
          </li>
          <li class="nav-item">
            <a href="https://www.youtube.com/channel/UCuLfhw7dJoKYbzBktNRgAkA" class="nav-link">
              <i class="bi bi-youtube" fill="currentColor">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
                  <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
                </svg>
              </i>
            </a>
          </li>
        </ul>
      </header>
    </div>`);
}

function footer() {
  document.write(`
    <footer class="footer mt-auto py-3 bg-light">
  <div class="container">
    <div class="d-flex justify-content-between">
    <span class="text-muted">Realização: </span>
    <a href="http://www.sbc.org.br/"><img src="${root()}img/footer_SBC.png" height="100"></a>
    <a href="https://icpc.global/"><img src="${root()}img/footer_ICPC.png" height="100"></a>
    </div>
  </div>
</footer>`);
}

function drawVisualization(rows) {
  function rankImg(year, phase, heightPx, rank, reverse=false) {
    var multiplier = (phase == "Nacional") ? (year > 2020 ? 4 : 3) : 1,
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

  google.charts.load('current', {packages: ['corechart', 'line']});
  var data = new google.visualization.DataTable();
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

  var options = {hAxis: {title: 'Ano'},
                 vAxis: {title: 'Rank', baseline: 1},
                 legend: {position: 'top'},
                 tooltip: {isHtml: true}};

  var lineChart = new google.visualization.LineChart(chart);
  lineChart.draw(data, options);
}



function yearsAgo(numYears) {return new Date().getFullYear() - numYears;}
// function firstYear() { return 1996; }
// function currentContest() {
//     date = new Date();
//     date.setFullYear(date.getFullYear() - firstYear() + 1);
//     return date.getFullYear();
// }


function resultTable(header, site_teams) {
  var RULE_COLORS = ['text-danger', 'text-primary', 'text-success'];

  function ruleHeaderCells() {
    var cells = '';
    for (i in RULE_COLORS)
      cells += `
        <th class='${RULE_COLORS[i]}' scope="col">regra ${Number(i) + 1}</th>`;
    return cells;
  }
  function ruleRowCells(teams) {
    var cells = '';
    for (i in RULE_COLORS)
      cells += `
      <td class='${RULE_COLORS[i]}'>${teams[i].length}</td>`;
    return cells;
  }
  function teamsCell(teams) {
    var cell = '';
    for (i in RULE_COLORS)
      for (team of teams[i])
        cell += `<span class="${RULE_COLORS[i]}">${team}</span><br>`;
    return cell;
  }
  function makeRow(site_teams) {
    var row = '';
    for (site_team of site_teams) {
      var [site, teams] = site_team;
      row += `
    <tr>
      <td scope="row">${site}</td>
      ${ruleRowCells(teams)}
      <td>${teamsCell(teams)}</td>
    </tr>`;
    }
    return row;
  }

  return `
<h3>${header}</h3>
<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">Sede</th>
      ${ruleHeaderCells()}
      <th scope="col">Times classificados</th>
    </tr>
  </thead>
  ${makeRow(site_teams)}
</table>`;
}

function accordion(name, items) {
  document.write(`
<div class="accordion" id="accordion${name}">`);
  for (item of items)
    accordionItem(`accordion${name}`, item[0], item[1], item[2]);
  document.write(`
</div>`);
}

function accordionItem(accordionName, itemName, itemHeader, itemBody) {
  document.write(`
  <div class="accordion-item">
    <h2 class="accordion-header" id="heading${itemName}">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${itemName}" aria-expanded="false" aria-controls="collapse${itemName}">
        ${itemHeader}
      </button>
    </h2>
    <div id="collapse${itemName}" class="accordion-collapse collapse" aria-labelledby="heading${itemName}" data-bs-parent="#${accordionName}">
      <div class="accordion-body">
        ${itemBody}
      </div>
    </div>
  </div>`);
}