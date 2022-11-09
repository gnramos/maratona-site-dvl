/**
 * Format the basic information for a contest.
 *
 * @param  {String} contest  name of directory with the contest files
 * @param  {Array}  problems list of problem names
 * @return {String}          the HTML with the formatted information
 */
function contestInfo(contest, problems) {
  var info = '';
  for (problem of problems)
    info += `\n  <li>${problem}</li>`;
  return `
<ul>
  <li><a href=${contest}/info_maratona.pdf">Informações</a></li>
  <li><a href=${contest}/maratona.pdf">Problemas</a></li>
  <li><a href=${contest}/packages.tar.gz">Entradas e Saídas</a></li>
</ul>
<p>
  Autores dos problemas:
</p>
<ol type="A">${info}
</ol>`;
}

/**
 * Format the links for BOCA reports of a contest.
 *
 * Links are hard-coded and files are expected to exist.
 *
 * @return {String} the HTML with the formatted information
 */
function contestReports() {
  return`
<ul>
  <li><a href="contest/score.html">Placar final</a></li>
  <li><a href="contest/runs.html">Lista de submissões</a></li>
  <li><a href="contest/clarifications.html">Lista de perguntas</a></li>
  <li><a href="contest/statistic.html">Estatísticas</a></li>
</ul>`;
}

/**
 * Build a gallery from a list of images.
 *
 * Gallery style is hard-coded, assumes all image files are in "img" directory.
 *
 * @param  {Array}  images list of image files
 * @return {String}        the HTML with the formatted information
 */
function gallery(images) {
  var items = '';
  for (img of images)
    items += `
  <div class="col-lg-3 col-md-4 col-6">
    <a href="img/${img}" class="d-block mb-4 h-100">
      <img class="img-fluid img-thumbnail" src="img/${img}" alt="${img}" onerror="this.style.display='none'"/>
    </a>
  </div>`;
        return `
<div class="row text-center text-lg-start">
${items}
</div>`;
      }

/**
 * Splits the list into gold/silver/bronze groups.
 *
 * @param  {Array}  medalists list of medalist objects
 * @return {Array}            [gold, silver, bronze] groups
 */
function splitbyMedal(medalists) {
  var teamsPerMedal = medalists.length / 3;
  return [medalists.slice(0, teamsPerMedal),                       // gold
          medalists.slice(teamsPerMedal, 2 * teamsPerMedal),       // silver
          medalists.slice(2 * teamsPerMedal)];                     // bronze
}

/**
 * Builds the results for teams that advanced in the 1st phase for a contest site.
 *
 * @param  {Array}  siteTeams list of sites and teams
 * @return {String}           the HTML with the formatted information
 */
function advancingTeams(results) {
  // results -> [siteName, [listOfRule1, listOfRule3, listOfRule3]]
  function ruleHeaderCells() {
    var cells = '';
    for (i in RULE_COLORS)
      cells += `\n        <th class='${RULE_COLORS[i]}' scope="col">Regra ${Number(i) + 1}</th>`;

    // A decidir se fica ou não
    return `<th scope="col">Tipo</th>`;

    return cells;
  }
  function ruleRowCells(teams) {
    var cells = '<td>';
    for (i in RULE_COLORS)
      for (team of teams[i])
        cells += `<span class="${RULE_COLORS[i]}"><strong>Regra ${Number(i) + 1}</strong></span><br>`;
    cells += "</td>";
    // A decidir se fica ou não
    // for (i in RULE_COLORS)
    //   cells += `
    //   <td class='${RULE_COLORS[i]}'>${teams[i].length}</td>`;

    return cells;
  }
  function teamsCell(teams) {
    var cell = '';
    for (i in RULE_COLORS)
      for (team of teams[i])
        cell += `<span class="${RULE_COLORS[i]}">${team}</span><br>`;
    return cell;
  }
  function makeRow(siteTeams) {
    var row = '';
    for (item of results) {
      var [site, teams] = item;
      row += `\n    <tr>
      <td scope="row">${site}</td>
        ${ruleRowCells(teams)}
      <td>${teamsCell(teams)}</td>
    </tr>`;
    }
    return row;
  }

  return `
<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">Sede</th>
        ${ruleHeaderCells()}
      <th scope="col">Times classificados</th>
    </tr>
  </thead>
  ${makeRow(results)}
</table>`;
}

/**
 * Builds a formatted ordered list of the teams.
 *
 * Assumes each team is defined as the array: [teamName, [contestants], [coaches]].
 * Assumes each team has a webp image of its members named according to its position in the list. For
 * example, that the first team has a picture named "team1.webp".
 *
 * @param  {Array}  teams list of teams
 * @param  {Int}    start starting number
 * @return {String}       the HTML with the formatted information
 */
function listTeams(teams, start=1) {
  var items = ``, images = [];
  for (i in teams){
    items += `
<li><strong>${teams[i][0]}:</strong> ${teams[i][1].join(', ')}${teams[i][2].length > 0 ? ' e coach(es) ' + teams[i][2].join(', ') : ''}.</li>`;
        images.push(teams[i][3] != undefined ? teams[i][3] : "team" + (Number(i) + start) + ".webp");
  }
  return `
\n<ol start=${start}>
${items}
</ol>
${gallery(images)}`;
}

/**
 * Builds a formatted presentation of the champion team.
 *
 * Assumes the team is defined as the array: [teamName, [contestants], [coaches]].
 *
 * @param  {Array}  team list of team information
 * @param  {Int}    img path to file with a picture of the team members
 * @return {String}       the HTML with the formatted information
 */
function showChampion(team, img) {
  return `
<div class="card mb-3">
  <!-- <h4 class='text-center'><strong>Campeões</strong></h4>-->
  <div class="row g-0">
  <!--  <div class="col-md-1">
      <img src="../../../img/trophy.png" class="img-fluid" style="max-height: 50px;" alt="...">
    </div>
    <div class="col-md-11">
      <div class="card-body">
        <h5 class="card-title">${team[0]}</h5>
        <p class="card-text">${team[1].join(', ')}${team[2].length > 0 ? ' e coach(es) ' + team[2].join(', ') : ''}.</p>
      </div>
    </div>-->
    <div class="col-md-9">
      <h4 class='text-center'><strong>Campeões</strong></h4>
      <div class="card-body">
        <h5 class="card-title">${team[0]}</h5>
        <p class="card-text">${team[1].join(', ')}${team[2].length > 0 ? ' e coach(es) ' + team[2].join(', ') : ''}.</p>
      </div>
    </div>
    <div class="col-md-3">
      <img class="img-fluid img-thumbnail" src="img/${img}">
    </div>
  </div>
</div>`;
}

/**
 * Return the year for specific events from the dir structure.
 *
 * @return {String} the year.
 */
function thisYear() {
  var url = window.location.pathname.split('/');
  return (isNaN(parseInt(url.at(-3))) ? url.at(-2) : url.at(-3));
}