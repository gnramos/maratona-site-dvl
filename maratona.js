function contact(text, ...args) {
    var mail = args.reduce((acc, cur) => acc + cur);
    document.write(`<a href="mailto:${mail}">${text}</a>`);
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
            <a class="nav-link dropdown-toggle ${currentDir == 'about' ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Sobre
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="${root()}about/index.html">O que é?</a></li>
              <li><a class="dropdown-item" href="${root()}about/rules.html">Regras</a></li>
              <li><a class="dropdown-item" href="${root()}about/format.html">Formato</a></li>
              <li><a class="dropdown-item" href="${root()}about/resources.html">Ambiente Computacional</a></li>
              <li><a class="dropdown-item" href="${root()}about/organization.html">Organização</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a href="${root()}participate.html" ${currentPage == 'participate.html' ? selected : unselected}>Inscreva-se</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle ${(currentPage == 'history.html') || (currentDir == 'institutions') ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Competições
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="https://maratona.sbc.org.br/final22.html">2022</a></li>
              <li><a class="dropdown-item" href="${root()}history/index.html">Anteriores</a></li>
              <li><a class="dropdown-item" href="https://gnramos.github.io/maratona-site">Estatísticas</a></li>
              <li><a class="dropdown-item" href="${root()}institutions/index.html">Instituições</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a href="${root()}contact.html" ${currentPage == 'contact.html' ? selected : unselected}>Contato</a>
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



function yearsAgo(numYears) {document.write(new Date().getFullYear() - numYears);}
function firstYear() { return 1996; }
function currentContest() {
    date = new Date();
    date.setFullYear(date.getFullYear() - firstYear() + 1);
    return date.getFullYear();
}

var romanNumbers = [ // [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
                    [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']];
function toRoman(num) {
  // http://blog.stevenlevithan.com/archives/javascript-roman-numeral-converter
  if (num === 0) return '';

  for (var i = 0; i < romanNumbers.length; i++)
    if (num >= romanNumbers[i][0])
      return romanNumbers[i][1] + toRoman(num - romanNumbers[i][0]);
}
