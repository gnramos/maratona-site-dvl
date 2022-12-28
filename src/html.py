from collections import defaultdict
import os
import re
from maratona import report
import unicodedata

REGION_DIR = {'Centro-Oeste': 'co', 'Nordeste': 'ne', 'Norte': 'no',
              'Sudeste': 'se', 'Sul': 'su'}

UF_STATE = {uf: state for state, uf in report.STATE_UF.items()}

BOOTSTRAP = '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'''


PHASES = ['PrimeiraFase', 'Nacional', 'Mundial']


class Result:
    def __init__(self, year, **ranks):
        self.year = int(year)
        self.ranks = {phase: str(ranks.get(phase, 'null')) for phase in PHASES}

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
                if self.ranks[phase] == 'null' and other.ranks[phase] != 'null':
                    return False
                if self.ranks[phase] != 'null' and other.ranks[phase] == 'null':
                    return True
                return int(self.ranks[phase]) > int(other.ranks[phase])
        return False

    def __str__(self):
        s = ', '.join(self.ranks.values())
        return f"[{self.year}, {s}]"

    @staticmethod
    def fill_and_list(results):
        if not results:
            return ''

        years = tuple(r.year for r in results)
        results.extend(Result(y)
                       for y in range(min(years) + 1, max(years))
                       if y not in years)
        return ',\n'.join(str(r) for r in sorted(results))

    @staticmethod
    def find_in_list(results, year):
        for r in results:
            if r.year == year:
                return r
        return None


class HTML:
    @staticmethod
    def path(uf):
        region = REGION_DIR[report.UF_REGION[uf.upper()]]
        return os.path.join('..', 'docs', 'escolas', region, uf.lower())

    @staticmethod
    def replace(template, file, replacements):
        with open(template, 'r') as f:
            content = f.read()
        for key, value in replacements.items():
            content = re.sub(key, value, content)
        with open(file, 'w') as f:
            f.write(content)

    @staticmethod
    def get_results(content):
        m = re.search(r'let results = \[([.\s\S]*?)\];', content)
        results = []
        for year, ranks in re.findall(r"\[(.*?), (.*?)\]", m.group(1)):
            kw_args = {phase: rank
                       for phase, rank in zip(PHASES, ranks.split(', '))}
            results.append(Result(year, **kw_args))
        return results

    @staticmethod
    def get_institution(content):
        m = re.search(r'bodyHeader\("(.*?)",', content)
        return m.group(1)

    @staticmethod
    def get_dropdown_items(content):
        p = r'<li><a class="dropdown-item" href="(.*?).html">(.*?)</a></li>'
        return [(short, full) for short, full in re.findall(p, content)]

    @staticmethod
    def dropdown_items(institutions):
        return '\n'.join(f'           <li><a class="dropdown-item" href="{short}.html">{full}</a></li>'
                         for short, full in sorted(institutions, key=lambda x: x[1]))


def create_school(uf, inst_short, inst_full, results):
    uf, path = uf.upper(), HTML.path(uf)

    if not os.path.isdir(path):
        os.makedirs(path)

    file = os.path.join(path, f'{inst_short}.html')
    results = Result.fill_and_list(results)

    HTML.replace('school_index.html', file,
                 {r'{BOOTSTRAP}': BOOTSTRAP, r'{RESULTS}': results,
                  r'{REGION}': report.UF_REGION[uf], r'{UF_FULL}': UF_STATE[uf],
                  r'{INSTITUTION}': inst_full, r'{INSTSHORTNAME}': inst_short})


def create_uf(uf, results, institutions):
    uf, path = uf.upper(), HTML.path(uf)

    if not os.path.isdir(path):
        os.makedirs(path)

    file = os.path.join(path, 'index.html')
    results = Result.fill_and_list(results)

    HTML.replace('uf_index.html', file,
                 {r'{BOOTSTRAP}': BOOTSTRAP, r'{RESULTS}': results,
                  r'{REGION}': report.UF_REGION[uf],
                  r'{UF_FULL}': UF_STATE[uf], r'{UF_SHORT}': uf.lower(),
                  r'{DROPDOWN_ITEMS}': HTML.dropdown_items(institutions)})


def update_school(uf, inst_short, year, phase, rank):
    file = os.path.join(HTML.path(uf), f'{inst_short}.html')

    with open(file, 'r') as f:
        content = f.read()

    results = HTML.get_results(content)
    inst_full = HTML.get_institution(content)

    for result in results:
        if result.year == year:
            result[phase] = rank
            break
    else:
        results.append(eval(f'Result({year}, {phase}={rank})'))

    create_school(uf, inst_short, inst_full, results)

    # If school being updated was the UF top ranking one and the update lowers
    # its rank, UF rank IS NOT CHANGED!
    file = os.path.join(HTML.path(uf), f'index.html')

    with open(file, 'r') as f:
        content = f.read()

    results = HTML.get_results(content)

    updated = True
    if result := Result.find_in_list(results, year):
        if result[phase] == 'null' or (result[phase] != 'null' and int(result[phase]) > int(rank)):
            result[phase] = rank
        else:
            updated = False
    else:
        results.append(eval(f'Result({year}, {phase}={rank})'))

    if updated:
        institutions = HTML.get_dropdown_items(content)
        create_uf(uf, results, institutions)


def df2dict(df):
    def normalize(name):
        name = re.sub(r'[^\w]', '', name.lower())
        return (unicodedata.normalize('NFD', name)
                .encode('ASCII', 'ignore')
                .decode('utf-8'))

    GROUPS = ['UF', 'instName', 'Year', 'Phase']
    df = df.sort_values(by=GROUPS + ['teamRank'])
    df_dict = {uf: defaultdict(dict) for uf in UF_STATE}
    for group, group_df in df.groupby(GROUPS):
        uf, inst, year, phase = group
        best_rank, year = int(group_df.iloc[0]['teamRank']), int(year)
        short = normalize(group_df.iloc[0]['instShortName'])
        if short not in df_dict[uf]:
            df_dict[uf][short] = {'Name': group_df.iloc[0]['instName'],
                                  'Results': []}
        if result := Result.find_in_list(df_dict[uf][short]['Results'], year):
            result[phase] = best_rank
        else:
            df_dict[uf][short]['Results'].append(
                eval(f'Result({year}, {phase}={best_rank})'))

    return df_dict


def create_files(df):
    for uf, inst_dict in df2dict(df).items():
        institutions, uf_results = [], []
        for short, info in inst_dict.items():
            create_school(uf, short, info['Name'], info['Results'])

            institutions.append((short, info['Name']))
            for result in info['Results']:
                if uf_result := Result.find_in_list(uf_results, result.year):
                    for phase in PHASES:
                        if uf_result[phase] == 'null' or (result[phase] != 'null' and int(uf_result[phase]) > int(result[phase])):
                            uf_result[phase] = result[phase]
                else:
                    uf_results.append(result)

        create_uf(uf, uf_results, institutions)


#     df = df[['Region', 'UF', 'Year', 'Phase', 'teamRank']]
#     df = df.drop_duplicates()
#     GROUPS = ['Region', 'UF', 'Year', 'Phase']
#     df = df.groupby(GROUPS).apply(lambda g: g[g['teamRank'] == g['teamRank'].min()])
#     from collections import defaultdict
#     results = defaultdict(list)
#     results = {}
#     for r in df.groupby(['Region', 'UF']):
#         print(r)
#     exit(0)

def gender_report(df):
    # É necessário ter todas as regiões, na mesma ordem, para garantir que as
    # cores serão iguais nos gráficos.
    d = {year: {'MALE': {phase: {region: 0 for region in REGION_DIR} for phase in PHASES},
                'FEMALE': {phase: {region: 0 for region in REGION_DIR} for phase in PHASES}}
         for year in df['Year'].unique()}

    GROUPS = ['Year', 'Phase', 'Region', 'sex']
    df = df[GROUPS + ['username']]
    for group, group_df in df.groupby(GROUPS):
        year, phase, region, gender = group
        d[year][gender][phase][region] = group_df.username.count()

    empty_phases = tuple((year, gender, phase)
                         for year, gender_d in d.items()
                         for gender, phases_d in gender_d.items()
                         for phase, regions_d in phases_d.items()
                         if sum(regions_d.values()) == 0)
    for year, gender, phase in empty_phases:
        del d[year][gender][phase]

    for year, gender_d in d.items():
        print(year)
        for gender, phases_d in gender_d.items():
            participants = ','.join(f"\n['{phase if phase != 'PrimeiraFase' else '1ªFase'}', '{REGION_DIR[r].upper()}', {count}]"
                                    for phase, regions_d in phases_d.items()
                                    for r, count in regions_d.items())
            print(f"let {gender.lower()} = [\n{participants}];")


if __name__ == '__main__':
    # update_school('df', 'unb', 2018, 'Nacional', 5)
    # exit(0)
    # raise 'Dashboard! Pie-chart de participantes por região, distribuição de desepenho por região?'
    #https://developers.google.com/chart/interactive/docs/gallery/controls
    # https://stackoverflow.com/questions/21411438/combining-two-types-of-category-filter-in-google-charts-api
    guess_uf = quiet = True

    pattern = re.compile(r'.*\d{4}_(1aFase|Nacional|Mundial)\.csv$')
    pattern = re.compile(r'.*20(19|20|21|22)_(1aFase|Nacional|Mundial)\.csv$')
    # pattern = re.compile(r'.*20(16|17|18|19)_(1aFase|Nacional|Programadores|Mundial)\.csv$')
    pattern = re.compile(r'.*20(16|17|18|19|20|21|22)_(1aFase|Nacional|Mundial)\.csv$')
    pattern = re.compile(r'.*20(20|21|22)_(1aFase|Nacional|Mundial)\.csv$')
    files = [os.path.join(root, f)
             for root, dirs, files in os.walk('../reports')
             for f in files if pattern.match(f)]

    df = None
    for file in sorted(files, reverse=True):
        year, phase, contest = report.process(file, guess_uf, not quiet)
        contest['Phase'] = phase if phase != '1aFase' else 'PrimeiraFase'
        contest['Year'] = year
        if df is None:
            df = contest
        else:
            df = df.append(contest, verify_integrity=True, ignore_index=True)

    df = df[(df.role == 'CONTESTANT') & (df.teamRank > 0) & (df.teamStatus == 'ACCEPTED')]
    # create_files(df)
    gender_report(df)

    exit(0)

    # df = df[(df['role'] == 'CONTESTANT') & (df['teamRank'] > 0)]
    # df = df[(df['teamStatus'] == 'ACCEPTED') & (df['teamRank'] > 0)]
    # df = df[['Region', 'UF', 'instName', 'instShortName', 'Year', 'Phase', 'teamName', 'teamRank']]
    # df = df.drop_duplicates()
    # # df = df.set_index(['Region', 'UF'])
    # GROUPS = ['Region', 'UF', 'instName', 'instShortName', 'Year', 'teamName']
    # # for group, group_df in df.groupby(GROUPS):
    # #     res = [group[4], 'null', 'null', 'null']
    # #     for row in group_df.itertuples():
    # #         res[['year', '1aFase', 'Nacional', 'Mundial'].index(row[-3])] = int(row[-1])

    # #     group_df = group_df.sort_values(by='teamRank')
    # #     print(group)
    # #     for row in group_df.pivot(index='teamName', columns='Phase', values='teamRank').iterrows():
    # #         name, ranks = row
    # #         ranks = ranks.to_list()
    # #         print(name, type(ranks), )
    # df = df.pivot(index='teamName', columns='Phase', values='teamRank')
    # for r in df.iterrows():
    #     print(r[0])
    # exit(0)

    # Campeões Regionais
    GROUPS = ['Region', 'UF', 'siteName', 'Year', 'Phase']
    regionais = df.groupby(GROUPS).apply(lambda g: g[g['teamRank'] == g['teamRank'].min()])
    # regionais = regionais[['Region', 'UF', 'Year', 'Phase', 'teamName', 'teamRank']].drop_duplicates()
    regionais = regionais.drop_duplicates()
    for group, groupdf in regionais.iterrows():
        print(group, groupdf)
    # print(df.groupby(GROUPS).apply(lambda g: g[g['teamRank'] == g['teamRank'].min()]))
    # for group, groupdf in df.groupby(GROUPS).apply(lambda g: g[g['teamRank'] == g['teamRank'].min()]).iterrows():
    #     region, uf, year, phase = group[:4]
    #     print(region, uf, year, phase, groupdf['teamName'], groupdf['teamRank'])
    # #     print(groupdf.pivot(index=['Region', 'UF', 'Year'], columns='Phase', values='teamRank'))

    # # print(df) # GROUPS = []
