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
  var gal = '';
  for (img of images)
    gal += `
  <div class="col-lg-3 col-md-4 col-6">
    <a href="img/${img}" class="d-block mb-4 h-100">
      <img class="img-fluid img-thumbnail" src="img/${img}">
    </a>
  </div>`;
        return `
<div class="row text-center text-lg-start">
${gal}
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
          medalists.slice(2 * teamsPerMedal, 3 * teamsPerMedal)];  // bronze
}

/**
 * Builds the results for teams that advanced in the 1st phase for a contest site.
 *
 * @param  {Array}  siteTeams list of sites and teams
 * @return {String}           the HTML with the formatted information
 */
function advancingTeams(results) {
  // results -> [siteName, [listOfRule1, listOfRule3, listOfRule3]]
  var RULE_COLORS = ['text-danger', 'text-primary', 'text-success'];

  function ruleHeaderCells() {
    var cells = '';
    for (i in RULE_COLORS)
      cells += `
        <th class='${RULE_COLORS[i]}' scope="col">regra ${Number(i) + 1}</th>`;

    // A decidir se fica ou não
    return `<th scope="col">Vaga</th>`;

    return cells;
  }
  function ruleRowCells(teams) {
    var cells = '<td>';
    for (i in RULE_COLORS)
      for (team of teams[i])
        cells += `<span class="${RULE_COLORS[i]}">regra ${Number(i) + 1}</span><br>`;
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
 * Return the year for specific events from the dir structure.
 *
 * @return {String} the year.
 */
function thisYear() {
  var url = window.location.pathname.split('/');
  return (isNaN(parseInt(url.at(-3))) ? url.at(-2) : url.at(-3));
}