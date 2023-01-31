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

Phase = namedtuple('Phase', 'title start')


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
        def __init__(self, phase_title, region, teams):
            self.region = region.upper()
            self.teams = int(teams)
            for phase in Event.Phases:
                if phase_title == str(phase):
                    self.phase = phase
                    break
            else:
                raise ValueError(f'Não existe fase "{phase_title}".')

        def __lt__(self, other):
            if self.phase != other.phase:
                return self.phase < other.phase
            return self.region < other.region

        def __str__(self):
            return f"['{self.phase}', '{self.region}', {self.teams}]"

    class Result:
        def __init__(self, year, **ranks):
            self.year = int(year)
            self.ranks = {phase.name: 'null' for phase in Event.Phases}
            for phase_title, rank in ranks.items():
                self[phase_title] = rank

        def __setitem__(self, key, value):
            self.ranks[key] = str(value)

        def __getitem__(self, key):
            return self.ranks[key]

        def __lt__(self, other):
            if self.year != other.year:
                return self.year < other.year
            for phase in reversed(Event.Phases):
                if self.ranks[phase.title] != other.ranks[phase.title]:
                    if self.ranks[phase.title] == 'null' != other.ranks[phase.title]:
                        return False
                    if self.ranks[phase.title] != 'null' == other.ranks[phase.title]:
                        return True
                    return int(self.ranks[phase.title]) > int(other.ranks[phase.title])
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
    def path_index(year, phase_name=''):
        path = os.path.join('..', 'docs', 'eventos', str(year), phase_name)
        index = os.path.join(path, 'index.html')
        return path, index

    @staticmethod
    def make_index(year):
        path, index = Event.path_index(year)
        os.makedirs(path, exist_ok=True)
        repl = {r'\[BOOTSTRAP\]': BOOTSTRAP}
        _sub_template('contest', repl, index)

    @staticmethod
    def make_phase_index(year, phase):
        # Não sobrescreve arquivo existente!
        if phase.exists_in(year):
            path, index = Event.path_index(year, phase.name)
            os.makedirs(path, exist_ok=True)

            if not os.path.isfile(index):
                Event.make_phase(year, phase)

    @staticmethod
    def make_phase(year, phase):
        if phase == Event.Phases.Nacional and year >= 2012:
            summer = f'''
         </script>
    <br>
    <p>
      Os times classificados para a Final Mundial serão convidados para o <a href="http://maratona.ic.unicamp.br/MaratonaVerao{year + 1}/">curso de treinamento</a> que ocorrerá na Unicamp.
    </p>
    <script type="text/javascript">'''
        else:
            summer = ''

        repl = {r'\[BOOTSTRAP\]': BOOTSTRAP,
                r'\[YEAR\]': str(year),
                r'\[PHASE_NAME\]': str(phase),
                r'\[SUMMER_SCHOOL\]': summer}
        path, index = Event.path_index(year, phase.name)
        _sub_template(phase.name, repl, index)

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
        def phase_participation(year, phase, df):
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

        for group, group_df in df.groupby(['Year', 'Phase']):
            year, phase_name = group
            phase = eval(f'Event.Phases.{phase_name}')
            year, num_teams = int(year), group_df.teamName.count() // 3

            Event.make_index(year)
            Event.make_phase_index(year, phase)
            phase_participation(year, phase, group_df)
            Event.update_history(year, phase.name, num_teams)

    @staticmethod
    def reset_index():
        path, index = Event.path_index('')
        Charts.Result.reset_file(index)

    @staticmethod
    def update_history(year, phase_name, teams):
        assert teams >= 0

        path, index = Event.path_index('')
        Charts.Result.update_file(index, year, phase_name, teams)

    class Phases(Enum):
        Zero = Phase('Fase 0', 2022)
        Primeira = Phase('1ª Fase', 2012)
        Nacional = Phase('Final Nacional', 1996)
        Mundial = Phase('Final Mundial', 1989)

        def __str__(self):
            return self.value.title

        def __lt__(self, other):
            return self.value.start > other.value.start

        def exists_in(self, year):
            return self.value.start <= year


class School:
    @staticmethod
    def make_institution_index(uf, inst_short, inst_full):
        uf = uf.upper()
        assert uf in UF_STATE

        path, file = School.path_index(uf, inst_short)
        repl = {r'\[BOOTSTRAP\]': BOOTSTRAP,
                r'\[FULL_NAME\]': inst_full,
                r'\[SHORT_NAME\]': inst_short}
        _sub_template('school', repl, file)

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
            year, phase_name, uf = group
            year = int(year)

            for g, gdf in group_df.groupby(['instShortName', 'instName', 'teamRank']):
                short, full, rank = g
                short, rank = normalize(short), int(rank)

                School.update_institution(uf, short, full, year, phase_name, rank)
                School.update_uf_result(uf, year, phase_name, rank)
                School.update_uf_dropdown(uf, short, full)

    @staticmethod
    def reset():
        for uf in UF_STATE:
            School.reset_uf(uf)
            School.reset_institutions(uf)

    @staticmethod
    def reset_institutions(uf):
        path, file = School.path_index(uf.upper())
        Charts.Result.reset_file(file)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != 'index.html' and file != f'{uf.lower()}.svg':
                    os.remove(os.path.join(path, file))

    @staticmethod
    def reset_uf(uf):
        path, index = School.path_index(uf.upper())
        repl = {r'<ul class="dropdown-menu" [.\s\S]*?</ul>': '<ul class="dropdown-menu" aria-labelledby="dropdownInstitutions">\n       </ul>'}
        file_sub(index, repl, index)

    @staticmethod
    def update_uf_result(uf, year, phase_name, rank):
        uf = uf.upper()
        path, index = School.path_index(uf)
        Charts.Result.update_file(index, year, phase_name, rank,
                                  replace_if_better=True)

    @staticmethod
    def update_uf_dropdown(uf, inst_short, inst_full):
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
        items = '\n  '.join(f'<li><a class="dropdown-item" href="{s}.html">{f}</a></li>'
                            for s, f in sorted(items, key=lambda x: x[1]))
        items = f'''<ul class="dropdown-menu" aria-labelledby="dropdownInstitutions">
{items}
       </ul>'''
        content = re.sub(pattern, items, content)
        with open(file, 'w') as f:
            f.write(content)

    @staticmethod
    def update_institution(uf, inst_short, inst_full, year, phase_name, rank):
        uf = uf.upper()
        path, file = School.path_index(uf, inst_short)

        if not os.path.isfile(file):
            School.make_institution_index(uf, inst_short, inst_full)

        Charts.Result.update_file(file, year, phase_name, rank, True)

        # If institutionl being updated was the UF top ranking one and the
        # update lowers its rank, UF rank IS NOT CHANGED!
        School.update_uf_result(uf, year, phase_name, rank)
