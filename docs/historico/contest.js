const RULE_TOOLTIP = ['Top 15!',
                      'Distribuição por sedes.',
                      'Vagas discricionárias.'];

/**
 * Return a list with the given problems.
 *
 * @param  {Array}  problems array with problems to be listed
 * @return {String}          the HTML with the formatted information
 */
function listProblems(problems) {
  let header = `
<p>
  Autores dos problemas:
</p>`;
  return header + makeList('ol', problems, 'type="A"');
}

/**
 * Format the basic information for a contest.
 *
 * @param  {String} contest  name of directory with the contest files
 * @param  {Array}  problems list of contest problems
 * @return {String}          the HTML with the formatted information
 */
function defaultInfo(contest, problems) {
  problems = (problems === undefined ? '' : listProblems(problems));
  return listLinks([[`${contest}/info_maratona.pdf`, 'Informações'],
                    [`${contest}/maratona.pdf`, 'Problemas'],
                    [`${contest}/packages.tar.gz`, 'Entradas e Saídas']]) + problems;
}

/**
 * Format the links for BOCA reports of a contest.
 *
 * Links are hard-coded and files are expected to exist.
 *
 * @param  {String} contest  name of directory with the contest files
 * @return {String} the HTML with the formatted information
 */
function defaultReport(contest) {
  return listLinks([[`${contest}/Score.html`, 'Placar final'],
                    [`${contest}/Runs.html`, 'Lista de submissões'],
                    [`${contest}/Clarifications.html`, 'Lista de perguntas'],
                    [`${contest}/Statistics.html`, 'Estatísticas']]);
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
  let items = '';
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
function splitByMedal(medalists) {
  let teamsPerMedal = medalists.length / 3;
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
  function ruleCell(teams) {
    let cell = '';
    for (i in RULE_COLORS)
      for (team of teams[i])
        cell += `<strong class="${RULE_COLORS[i]}" ${tooltip(i)}>Regra ${Number(i) + 1}</strong><br>`;

    return cell;
  }
  function teamsCell(teams) {
    let cell = '';
    for (i in RULE_COLORS)
      for (team of teams[i])
        cell += `<span class="${RULE_COLORS[i]}">${team}</span><br>`;
    return cell;
  }
  function makeRows(siteTeams) {
    let rows = '';
    for (item of results) {
      let [site, teams] = item;
      rows += `
    <tr>
      <td scope="row">${site}</td>
      <td>${ruleCell(teams)}</td>
      <td>${teamsCell(teams)}</td>
    </tr>`;
    }
    return rows;
  }

  return `
<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">Sede</th>
      <th scope="col">Tipo</th>
      <th scope="col">Classificados</th>
    </tr>
  </thead>
  ${makeRows(results)}
</table>`;
}

/**
 * Builds a formatted ordered list of the teams.
 *
 * Assumes each team is defined as the array: [teamName, [contestants], [coaches], teamPicture].
 * Assumes each team has a webp image of its members named according to its position in the list. For
 * example, that the first team has a picture named "team1.webp".
 *
 * @param  {Array}  teams list of teams
 * @param  {Int}    start starting number
 * @return {String}       the HTML with the formatted information
 */
function listTeams(teams, start=1) {
  let items = '', images = [];
  for (i in teams) {
    let [name, contestants, coaches, img] = teams[i];
    contestants = contestants.join(', ');
    coaches = (coaches.length > 0 ? ' e coach(es) ' + coaches.join(', ') : '');
    items += `
<li><strong>${name}:</strong> ${contestants}${coaches}.</li>`;
        images.push(img != undefined ? img : "team" + (Number(i) + start) + ".webp");
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
  let [name, contestants, coaches] = team;
  contestants = contestants.join(', ');
  coaches = (coaches.length > 0 ? ' e coach(es) ' + coaches.join(', ') : '');
  return `
<div class="card mb-3">
  <div class="row g-0">
    <div class="col-md-9">
      <h4 class='text-center'><strong>Campeões</strong></h4>
      <div class="card-body">
        <h5 class="card-title">${name}</h5>
        <p class="card-text">${contestants}${coaches}.</p>
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
  let url = window.location.pathname.split('/');
  return (isNaN(parseInt(url.at(-3))) ? url.at(-2) : url.at(-3));
}

/**
 * Returns breadcrumbs for a contest from the dir structure.
 *
 * @return {String} the breadcrumbs.
 */
function makeBreadcrumbs() {
  let url = window.location.pathname.split('/');
  if (url.at(-3) == CURRENT_YEAR)
    return '';

  let breadcrumbItems = [];
  let prefix = (url.at(-1) == 'index.html' ? '../../' : '../');
  let i = (url.at(-1) == 'index.html' ? -3 : -2);
  while (url.at(i) != 'historico') {
    breadcrumbItems.push([`${prefix}${url.at(i)}/index.html`, url.at(i)]);
    prefix += '../';
    i -= 1;
  }
  breadcrumbItems.push([`${prefix}${url.at(i)}/index.html`, 'Maratonas']);
  breadcrumbItems.reverse();
  let lis = '';
  for (item of breadcrumbItems)
    lis += `\n<li class="breadcrumb-item"><a href="${item[0]}">${item[1]}</a></li>`;
  return `
        <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb">
          <ol class="breadcrumb">
            ${lis}
          </ol>
        </nav>`;
}

/**
 * Returns a tooltip.
 *
 * @return {String} the tooltip.
 */
function tooltip(i) {
  return `data-toggle="tooltip" data-html="true" title="${RULE_TOOLTIP[i]}"`;
}