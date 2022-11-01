function contest_info(contest, problems) {
  var info = '';
  for (problem of problems)
    info += `\n  <li>${problem}</li>`;
  return `
<ul>
  <li><a href=${contest}/info_maratona.pdf">Informações</a></li>
  <li><a href=${contest}/maratona.pdf">Problemas da prova</a></li>
  <li><a href=${contest}/packages.tar.gz">Entradas e Saídas dos problemas</a></li>
</ul>
<p>
  Autores dos problemas:
</p>
<ol type="A">${info}
</ol>`;
}

function contest_reports() {
  return`
<ul>
  <li><a href="contest/score.html">Placar final</a></li>
  <li><a href="contest/runs.html">Lista de submissões</a></li>
  <li><a href="contest/clarifications.html">Lista de perguntas</a></li>
  <li><a href="contest/statistic.html">Estatísticas</a></li>
</ul>`;
}

function medals(medalists) {
  var teamsPerMedal = medalists.length / 3;
  return [medalists.slice(0, teamsPerMedal),                         // gold
          medalists.slice(teamsPerMedal, 2 * teamsPerMedal),       // silver
          medalists.slice(2 * teamsPerMedal, 3 * teamsPerMedal)];  // bronze
}

function resultTable(site_teams) {
  // site_teams -> [siteName, [list_of_teams_rule1, list_of_teams_rule3, list_of_teams_rule3]]
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