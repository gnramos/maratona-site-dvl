from collections import namedtuple
from enum import Enum
import os
import re
from report import STATE_UF, UF_REGION, normalize


REGION_DIR = {'Centro-Oeste': 'co', 'Nordeste': 'ne', 'Norte': 'no',
              'Sudeste': 'se', 'Sul': 'su'}

UF_STATE = {uf: state for state, uf in STATE_UF.items()}

BOOTSTRAP = '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'''

Phase = namedtuple('Phase', 'html_name start')


def file_sub(file_in, repl, file_out, count=0):
    with open(file_in, 'r') as f:
        content = f.read()
    for key, value in repl.items():
        content = re.sub(key, value, content, count=count)
    with open(file_out, 'w') as f:
        f.write(content)


def _sub_template(template, repl, file, count=0):
    template = os.path.join('templates', f'{template}.html')
    file_sub(template, repl, file, count)


def _get_array(file, array_name):
    with open(file) as f:
        if matches := re.search(f'let {array_name} = \\[([.\\s\\S]*?)\\];', f.read()):
            return [item for item in re.findall(r"(\[.*?\])", matches.group(1))]
    return []


class Charts:
    class GenderParticipation:
        def __init__(self, phase_html_name, region, teams):
            self.region = region.upper()
            self.teams = int(teams)
            for phase in Event.Phases:
                if phase_html_name == phase.value.html_name:
                    self.phase = phase
                    break

        def __lt__(self, other):
            if self.phase != other.phase:
                return self.phase < other.phase
            return self.region < other.region

        def __str__(self):
            return f"['{self.phase}', '{self.region}', {self.teams}]"

    class Result:
        def __init__(self, year, **ranks):
            self.year = int(year)
            # Sempre lista todas as fases, nesta ordem!
            self.ranks = {phase.name: 'null' for phase in Event.Phases}
            for phase_html_name, rank in ranks.items():
                self[phase_html_name] = rank

        def __setitem__(self, key, value):
            self.ranks[key] = str(value)

        def __getitem__(self, key):
            return self.ranks[key]

        def __lt__(self, other):
            if self.year != other.year:
                return self.year < other.year
            for phase in reversed(Event.Phases):
                if self.ranks[phase.html_name] != other.ranks[phase.html_name]:
                    if self.ranks[phase.html_name] == 'null' != other.ranks[phase.html_name]:
                        return False
                    if self.ranks[phase.html_name] != 'null' == other.ranks[phase.html_name]:
                        return True
                    return int(self.ranks[phase.html_name]) > int(other.ranks[phase.html_name])
            return False

        def __str__(self):
            s = ', '.join(self.ranks.values())
            return f"[{self.year}, {s}]"

        @staticmethod
        def update_file(file, year, phase_name, value, replace_if_better=False):
            pattern = re.compile(r'\[(.*?), (.*?)\]')
            results = []
            for result in _get_array(file, 'results'):
                y, ranks = pattern.match(result).groups(1)
                ranks = ranks.split(', ')
                results.append(Charts.Result(y, **{phase.name: rank
                                                   for phase, rank in zip(Event.Phases, ranks)
                                                   if rank != 'null'}))
            for result in results:
                if result.year == year:
                    if replace_if_better:
                        if result[phase_name] == 'null' or (result[phase_name] != 'null' and int(result[phase_name]) > value):
                            result[phase_name] = value
                    else:
                        result[phase_name] = value
                    break
            else:
                results.append(Charts.Result(year, **{phase_name: value}))
            results = ',\n'.join(str(r) for r in sorted(results))

            repl = {r'let results = \[([.\s\S]*?)\];': f'let results = [\n{results}];'}
            file_sub(file, repl, file)

        @staticmethod
        def reset_file(file):
            repl = {r'let results = \[[.\s\S]*?\];': 'let results = [];'}
            file_sub(file, repl, file)


class Event:
    @staticmethod
    def create(year):
        path, index = Event.path_index(year)
        os.makedirs(path, exist_ok=True)
        repl = {r'\[BOOTSTRAP\]': BOOTSTRAP}
        _sub_template('contest', repl, index)

    @staticmethod
    def path_index(year):
        path = os.path.join('..', 'docs', 'eventos', str(year))
        index = os.path.join(path, 'index.html')
        return path, index

    @staticmethod
    def update_index(year, phase, region, gender, teams):
        assert region.lower() in REGION_DIR.values()
        assert teams >= 0

        path, index = Event.path_index(year)

        if not os.path.isfile(index):
            Event.Index.make(year)

        participations = [Charts.GenderParticipation(*eval(item))
                          for item in _get_array(index, gender)]
        for part in participations:
            if phase == part.phase and region == part.region:
                part.teams = teams
                break
        else:
            participations.append(Charts.GenderParticipation(str(phase), region, teams))
        participations = ',\n'.join(str(p) for p in sorted(participations))

        repl = {f'let {gender} = \\[([.\\s\\S]*?)\\];': f'let {gender} = [\n{participations}];'}
        file_sub(index, repl, index)

    @staticmethod
    def process(df):
        def gender_participation(year, phase, df):
            d = {gender: {region: 0 for region in REGION_DIR}
                 for gender in df['sex'].unique()}

            for group, group_df in df.groupby(['Region', 'sex']):
                region, gender = group
                d[gender][region] = group_df.username.count()

            for gender, region_d in d.items():
                if any(count for count in region_d.values()):
                    for region, count in region_d.items():
                        Event.update_index(year, phase,
                                           REGION_DIR[region].upper(),
                                           gender.lower(), count)

        def team_participation(year, phase, num_teams):
            path, index = Event.path_index('')
            Charts.Result.update_file(index, year, phase.name, num_teams)

        for group, group_df in df.groupby(['Year', 'Phase']):
            year, phase_name = group
            phase = eval(f'Event.Phases.{phase_name}')
            year, num_teams = int(year), group_df.teamName.count() // 3

            Event.create(year)
            phase.create(year)
            gender_participation(year, phase, group_df)
            team_participation(year, phase, num_teams)

    @staticmethod
    def reset_index():
        path, index = Event.path_index('')
        Charts.Result.reset_file(index)

    class Phases(Enum):
        Zero = Phase('Fase 0', 2022)
        Primeira = Phase('1ª Fase', 2012)
        Nacional = Phase('Final Nacional', 1996)
        Mundial = Phase('Final Mundial', 1989)

        def __str__(self):
            return self.value.html_name

        def __lt__(self, other):
            return self.value.start > other.value.start

        def create(self, year):
            def summerschool():
                if self != Event.Phases.Nacional or year < 2012:
                    return ''
                return f'''
         </script>
    <br>
    <p>
      Os times classificados para a Final Mundial serão convidados para o <a href="http://maratona.ic.unicamp.br/MaratonaVerao{year + 1}/">curso de treinamento</a> que ocorrerá na Unicamp.
    </p>
    <script type="text/javascript">'''

            if self.value.start > year:
                print(f'{self.value.html_name} só existe a partir {self.value.start}.')
                return

            path, index = self.path_index(year)
            if os.path.isfile(index):
                print(f'Já existe um arquivo para {self.value.html_name} em {year}.')
                return

            os.makedirs(path, exist_ok=True)

            repl = {r'\[BOOTSTRAP\]': BOOTSTRAP,
                    r'\[YEAR\]': str(year),
                    r'\[PHASE_NAME\]': self.value.html_name,
                    r'\[SUMMER_SCHOOL\]': summerschool()}
            _sub_template(self.name, repl, index)

        def path_index(self, year):
            path = os.path.join('..', 'docs', 'eventos', str(year), self.name)
            index = os.path.join(path, 'index.html')
            return path, index


class School:
    @staticmethod
    def create(uf, inst_short, inst_full):
        uf = uf.upper()

        path, file = School.path_index(uf, inst_short)
        repl = {r'\[BOOTSTRAP\]': BOOTSTRAP,
                r'\[FULL_NAME\]': inst_full,
                r'\[SHORT_NAME\]': inst_short}
        _sub_template('school', repl, file)

    @staticmethod
    def path_index(uf, school_name):
        region = REGION_DIR[UF_REGION[uf.upper()]]
        path = os.path.join('..', 'docs', 'escolas', region, uf.lower())
        index = os.path.join(path, f'{school_name}.html')
        return path, index

    @staticmethod
    def process(df):
        GROUPS = ['Year', 'Phase', 'UF']
        for group, group_df in df.groupby(GROUPS):
            year, phase_name, uf = group
            year = int(year)

            for g, gdf in group_df.groupby(['instShortName', 'instName', 'teamRank']):
                short, full, rank = g
                short, rank = normalize(short), int(rank)

                School.update(uf, short, full, year, phase_name, rank)

    @staticmethod
    def reset():
        for uf in UF_STATE:
            # Dropdown
            path, index = School.path_index(uf.upper(), 'index')
            repl = {r'<ul class="dropdown-menu" [.\s\S]*?</ul>': '<ul class="dropdown-menu" aria-labelledby="dropdownInstitutions">\n       </ul>'}
            file_sub(index, repl, index)

            # School files
            Charts.Result.reset_file(index)
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file != 'index.html' and file != f'{uf.lower()}.svg':
                        os.remove(os.path.join(path, file))

    @staticmethod
    def update(uf, inst_short, inst_full, year, phase_name, rank):
        uf = uf.upper()
        path, file = School.path_index(uf, inst_short)

        if not os.path.isfile(file):
            School.create(uf, inst_short, inst_full)

        Charts.Result.update_file(file, year, phase_name, rank, True)

        # If institutionl being updated was the UF top ranking one and the
        # update lowers its rank, UF rank IS NOT CHANGED!
        path, index = School.path_index(uf, 'index')
        Charts.Result.update_file(index, year, phase_name, rank,
                                  replace_if_better=True)

        # Update dropdown
        with open(index, 'r') as f:
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

        items = '\n  '.join(f'<li><a class="dropdown-item" href="{s}.html">{f}</a></li>'
                            for s, f in sorted(items, key=lambda x: x[1]))
        items = f'''<ul class="dropdown-menu" aria-labelledby="dropdownInstitutions">
{items}
       </ul>'''
        repl = {r'<ul class="dropdown-menu" [.\s\S]*?</ul>': items}
        file_sub(index, repl, index)
