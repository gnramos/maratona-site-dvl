from collections import defaultdict
import os
import re
from report import STATE_UF, UF_REGION, normalize


# Fases / ano de implementação.
PHASES = {'Zero': 2022, 'Primeira': 2004, 'Nacional': 1996, 'Mundial': 1989}
PHASE_TITLE = {'Zero': 'Fase 0', 'Primeira': '1ª Fase',
               'Nacional': 'Final Nacional', 'Mundial': 'Final Mundial'}
TITLE_PHASE = {title: phase for phase, title in PHASE_TITLE.items()}

REGION_DIR = {'Centro-Oeste': 'co', 'Nordeste': 'ne', 'Norte': 'no',
              'Sudeste': 'se', 'Sul': 'su'}

UF_STATE = {uf: state for state, uf in STATE_UF.items()}

BOOTSTRAP = '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'''


def _sub_in_template(template, repl, new_file):
    template = os.path.join('templates', f'{template}.html')
    with open(template, 'r') as f:
        content = f.read()
    for key, value in repl.items():
        content = re.sub(key, value, content)
    with open(new_file, 'w') as f:
        f.write(content)


def _get_array(name, content):
    matches = re.search(f'let {name} = \\[([.\\s\\S]*?)\\];', content)
    return [item for item in re.findall(r"(\[.*?\])", matches.group(1))]


class ChartInfo:
    class GenderParticipation:
        phases = list(PHASES)

        def __init__(self, phase, region, teams):
            self.phase = PHASES.get(phase, TITLE_PHASE[phase])
            self.region = region.upper()
            self.teams = int(teams)

        def __lt__(self, other):
            if other is None:
                return True
            if self.phase != other.phase:
                return ChartInfo.GenderParticipation.phases.index(self.phase) < ChartInfo.GenderParticipation.phases.index(other.phase)
            return self.region < other.region

        def __str__(self):
            return f"['{PHASE_TITLE[self.phase]}', '{self.region}', {self.teams}]"

    class Result:
        def __init__(self, year, **ranks):
            self.year = int(year)
            self.ranks = {}
            for p in PHASES:
                if (rank := ranks.get(p, 'null')) != 'null':
                    self.ranks[p] = f'{float(rank):.0f}'
                else:
                    self.ranks[p] = str(rank)

        def __setitem__(self, key, value):
            self.ranks[key] = str(value)

        def __getitem__(self, key):
            return self.ranks[key]

        def __lt__(self, other):
            if other is None:
                return True
            if self.year != other.year:
                return self.year < other.year
            for phase in reversed(PHASES):
                if self.ranks[phase] != other.ranks[phase]:
                    if self.ranks[phase] == 'null' != other.ranks[phase]:
                        return False
                    if self.ranks[phase] != 'null' == other.ranks[phase]:
                        return True
                    return int(self.ranks[phase]) > int(other.ranks[phase])
            return False

        def __str__(self):
            s = ', '.join(self.ranks.values())
            return f"[{self.year}, {s}]"

        @staticmethod
        def update_file(file, year, phase, value, replace_if_better=False):
            with open(file, 'r') as f:
                content = f.read()

            pattern = re.compile(r'\[(.*?), (.*?)\]')
            results = []
            for result in _get_array('results', content):
                y, ranks = pattern.match(result).groups(1)
                ranks = ranks.split(', ')
                results.append(ChartInfo.Result(y, **{phase: rank
                                                for phase, rank in zip(PHASES, ranks)}))
            for result in results:
                if result.year == year:
                    if replace_if_better:
                        if result[phase] == 'null' or (result[phase] != 'null' and int(result[phase]) > value):
                            result[phase] = value
                    else:
                        result[phase] = value
                    break
            else:
                results.append(ChartInfo.Result(year, **{phase: value}))
            results = ',\n'.join(str(r) for r in sorted(results))

            pattern = r'let results = \[([.\s\S]*?)\];'
            results = f'let results = [\n{results}];'
            content = re.sub(pattern, results, content)

            with open(file, 'w') as f:
                f.write(content)

        @staticmethod
        def reset_file(file):
            with open(file, 'r') as f:
                content = f.read()
            pattern = re.compile(r'let results = \[[.\s\S]*?\];')
            content = re.sub(pattern, 'let results = [];', content)
            with open(file, 'w') as f:
                f.write(content)


class Contest:
    @staticmethod
    def path_index(year, phase=''):
        path = os.path.join('..', 'docs', 'historico', str(year), phase)
        index = os.path.join(path, 'index.html')
        return path, index

    class Index:
        @staticmethod
        def make(year):
            path, index = Contest.path_index(year)
            os.makedirs(path, exist_ok=True)
            _sub_in_template('contest', {r'{BOOTSTRAP}': BOOTSTRAP}, index)

        @staticmethod
        def update(year, phase, region, gender, teams):
            assert phase in PHASES
            assert region.lower() in REGION_DIR.values()
            assert gender in ('male', 'female')
            assert teams >= 0

            path, index = Contest.path_index(year)

            if not os.path.isfile(index):
                Contest.Index.make(year)

            with open(index, 'r') as f:
                content = f.read()

            participations = [ChartInfo.GenderParticipation(*eval(item))
                              for item in _get_array(gender, content)]
            for p in participations:
                if phase == p.phase and region == p.region:
                    p.teams = teams
                    break
            else:
                participations.append(ChartInfo.GenderParticipation(phase, region, teams))
            participations = ',\n'.join(str(p) for p in sorted(participations))

            pattern = f'let {gender} = \\[([.\\s\\S]*?)\\];'
            participations = f'let {gender} = [\n{participations}];'
            content = re.sub(pattern, participations, content)

            with open(index, 'w') as f:
                f.write(content)

    class Phase:
        @staticmethod
        def make(year, phase):
            # Não sobrescreve arquivo existente!
            assert phase in PHASES

            if (int(year) >= PHASES[phase]):
                path, index = Contest.path_index(year, phase)
                os.makedirs(path, exist_ok=True)

                if not os.path.isfile(index):
                    replacements = {'{PHASE}': PHASE_TITLE[phase]}
                    if phase == 'Mundial':
                        repl["let results = '';"] = f'''let results = `
<p>
  Os resultados oficiais estão disponíveis no <a href="https://icpc.global/community/results-{int(year) + 1}">site do ICPC</a>.
</p>
`;'''

                    _sub_in_template('phase', repl, index)

    @staticmethod
    def process(df):
        def phase_participation(df):
            # É necessário ter todas as regiões, na mesma ordem, para garantir
            # que as cores serão iguais nos gráficos.
            d = {gender: {region: 0 for region in REGION_DIR}
                 for gender in df['sex'].unique()}

            # Contagem da participação
            for group, group_df in df.groupby(['Region', 'sex']):
                region, gender = group
                d[gender][region] = group_df.username.count()

            for gender, region_d in d.items():
                if any(count for count in region_d.values()):
                    for region, count in region_d.items():
                        Contest.Index.update(year, phase,
                                             REGION_DIR[region].upper(),
                                             gender.lower(), count)

        for group, group_df in df.groupby(['Year', 'Phase']):
            year, phase = group
            year = int(year)

            Contest.Phase.make(year, phase)
            phase_participation(group_df)
            Contest.History.update(year, phase, group_df.teamName.count() // 3)

    class History:
        @staticmethod
        def index():
            return os.path.join('..', 'docs', 'historico', 'index.html')

        @staticmethod
        def reset():
            ChartInfo.Result.reset_file(Contest.History.index())

        @staticmethod
        def update(year, phase, teams):
            assert phase in PHASES
            assert teams >= 0

            index = Contest.History.index()
            ChartInfo.Result.update_file(index, year, phase, teams)


class School:
    @staticmethod
    def reset():
        for uf in UF_STATE:
            School.UF.reset(uf)
            School.Institution.reset(uf)

    @staticmethod
    def path_index(uf, institution='index'):
        region = REGION_DIR[UF_REGION[uf.upper()]]
        path = os.path.join('..', 'docs', 'escolas', region, uf.lower())
        index = os.path.join(path, f'{institution}.html')
        return path, index

    @staticmethod
    def process(df):
        GROUPS = ['Year', 'Phase', 'UF']
        for group, group_df in df.groupby(GROUPS):
            year, phase, uf = group
            year = int(year)

            for g, gdf in group_df.groupby(['instShortName', 'instName', 'teamRank']):
                short, full, rank = g
                short, rank = normalize(short), int(rank)

                School.Institution.update(uf, short, full, year, phase, rank)
                School.UF.update_result(uf, year, phase, rank)
                School.UF.update_dropdown(uf, short, full)

    class UF:
        @staticmethod
        def reset(uf):
            path, index = School.path_index(uf.upper())
            with open(index, 'r') as f:
                content = f.read()
            pattern = r'<ul class="dropdown-menu" [.\s\S]*?</ul>'
            replace = '<ul class="dropdown-menu" aria-labelledby="dropdownInstitutions">\n       </ul>'
            content = re.sub(pattern, replace, content)
            with open(index, 'w') as f:
                f.write(content)

        @staticmethod
        def update_result(uf, year, phase, rank):
            uf = uf.upper()
            assert uf in UF_STATE
            assert phase in PHASES
            assert rank >= 0

            path, index = School.path_index(uf)
            ChartInfo.Result.update_file(index, year, phase, rank, replace_if_better=True)

        @staticmethod
        def update_dropdown(uf, inst_short, inst_full):
            uf = uf.upper()
            assert uf in UF_STATE

            path, file = School.path_index(uf)
            with open(file, 'r') as f:
                content = f.read()

            pattern = r'<li><a class="dropdown-item" href="(.*?).html">(.*?)</a></li>'
            items = [[s, f] for s, f in re.findall(pattern, content)]
            for item in items:
                if item[0] == inst_short:
                    if item[1] != inst_full:
                        item[1] = inst_full
                    break
            else:
                items.append([inst_short, inst_full])

            pattern = r'<ul class="dropdown-menu" [.\s\S]*?</ul>'
            items = '\n'.join(f'<li><a class="dropdown-item" href="{s}.html">{f}</a></li>'
                              for s, f in sorted(items, key=lambda x: x[1]))
            items = f'''<ul class="dropdown-menu" aria-labelledby="dropdownInstitutions">
{items}
       </ul>'''
            content = re.sub(pattern, items, content)

            with open(file, 'w') as f:
                f.write(content)

    class Institution:
        @staticmethod
        def reset(uf):
            path, file = School.path_index(uf.upper())
            ChartInfo.Result.reset_file(file)
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file != 'index.html' and file.endswith('.html'):
                        os.remove(os.path.join(path, file))

        @staticmethod
        def make(uf, inst_short, inst_full):
            uf = uf.upper()
            assert uf in UF_STATE

            path, file = School.path_index(uf, inst_short)
            repl = {r'{BOOTSTRAP}': BOOTSTRAP, r'{INSTITUTION}': inst_full,
                    r'{INSTSHORTNAME}': inst_short}
            _sub_in_template('school', repl, file)

        @staticmethod
        def update(uf, inst_short, inst_full, year, phase, rank):
            uf = uf.upper()
            assert uf in UF_STATE
            assert phase in PHASES
            assert rank > 0

            path, file = School.path_index(uf, inst_short)

            if not os.path.isfile(file):
                School.Institution.make(uf, inst_short, inst_full)

            ChartInfo.Result.update_file(file, year, phase, rank, True)

            # If institutionl being updated was the UF top ranking one and the
            # update lowers its rank, UF rank IS NOT CHANGED!
            School.UF.update_result(uf, year, phase, rank)
