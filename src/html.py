from collections import defaultdict, namedtuple
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
        self.year = year
        self.ranks = {phase: ranks.get(phase, 'null') for phase in PHASES}

    def __setitem__(self, key, value):
        self.ranks[key] = value

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
                return self.ranks[phase] > other.ranks[phase]
        return False

    def __str__(self):
        s = ', '.join(str(self.ranks[phase]) for phase in PHASES)
        return f"[{self.year}, {s}]"

    @staticmethod
    def fill(results):
        if results:
            years = tuple(result.year for result in results)
            results.extend(Result(y)
                           for y in range(min(years) + 1, max(years))
                           if y not in years)
            results.sort()

    @staticmethod
    def find_in_list(results, year):
        for result in results:
            if result.year == year:
                return result
        return None


class HTML:
    @staticmethod
    def path(uf):
        region = report.UF_REGION[uf.upper()]
        return os.path.join('..', 'docs', 'escolas', REGION_DIR[region], uf.lower())

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
        for year, ranks in re.findall(r"\[(.*?), (.*?)\]", m.group(0)):
            kw_args = {phase: rank
                       for phase, rank in zip(PHASES, ranks.split(', '))}
            results.append(Result(year, **kw_args))
        return results

    @staticmethod
    def get_institution(content):
        m = re.search(r'bodyHeader\("(.*?)",', content)
        return m.group(1)

    @staticmethod
    def get_dropdown_institutions(content):
        p = r'<li><a class="dropdown-item" href="(.*?).html">(.*?)</a></li>'
        return [(short, full) for short, full in re.findall(p, content)]


def create_school(uf, inst_short, inst_full, results):
    uf, path = uf.upper(), HTML.path(uf)

    if not os.path.isdir(path):
        os.makedirs(path)

    file = os.path.join(path, f'{inst_short}.html')
    Result.fill(results)
    results = ',\n'.join(str(r) for r in sorted(results))

    HTML.replace('school_index.html', file,
                 {r'{BOOTSTRAP}': BOOTSTRAP, r'{RESULTS}': results,
                  r'{REGION}': report.UF_REGION[uf], r'{UF_FULL}': UF_STATE[uf],
                  r'{INSTITUTION}': inst_full, r'{INSTSHORTNAME}': inst_short})


def create_uf(uf, results, institutions):
    uf, path = uf.upper(), HTML.path(uf)

    if not os.path.isdir(path):
        os.makedirs(path)

    file = os.path.join(path, 'index.html')
    Result.fill(results)
    results = ',\n'.join(str(r) for r in sorted(results))
    dropdown = '\n'.join(f'           <li><a class="dropdown-item" href="{short}.html">{full}</a></li>'
                         for short, full in sorted(institutions, key=lambda x: x[1]))

    HTML.replace('uf_index.html', file,
                 {r'{BOOTSTRAP}': BOOTSTRAP, r'{RESULTS}': results,
                  r'{REGION}': report.UF_REGION[uf],
                  r'{UF_FULL}': UF_STATE[uf], r'{UF_SHORT}': uf.lower(),
                  r'{DROPDOWN_ITEMS}': dropdown})


def update_school(uf, inst_short, year, phase, rank):
    file = os.path.join(HTML.path(uf), f'{inst_short}.html')

    with open(file, 'r') as f:
        content = f.read()

    results = HTML.get_results(content)
    inst_full = HTML.get_institution(content)

    for result in results:
        if result.year == year:
            result[phase] = str(rank)
            break
    else:
        results.append(eval(f'Result({year}, {phase}={rank})'))

    create_school(uf, inst_short, inst_full, results)

    # TO-DO
    # If school being updated was the top ranking and update is to lower its rank,
    # UF rank IS NOT CHANGED
    file = os.path.join(HTML.path(uf), f'index.html')

    with open(file, 'r') as f:
        content = f.read()

    results = HTML.get_results(content)
    institutions = HTML.get_dropdown_institutions(content)

    updated = True

    if result := Result.find_in_list(results, year):
        if result[phase] == 'null' or (result[phase] != 'null' and result[phase] > rank):
            result[phase] = rank
        else:
            updated = False
    else:
        results.append(result)

    if updated:
        create_uf(uf, results, institutions)


def df2dict(df):
    df = df[(df['role'] == 'CONTESTANT') & (df['teamRank'] > 0)]
    GROUPS = ['UF', 'instName', 'Year', 'Phase']
    df = df.sort_values(by=GROUPS + ['teamRank'])
    df_dict = {uf: defaultdict(dict) for uf in UF_STATE}
    for group, group_df in df.groupby(GROUPS):
        uf, inst, year, phase = group
        best_rank, year = int(group_df.iloc[0]['teamRank']), int(year)
        short_name = unicodedata.normalize('NFD', group_df.iloc[0]['instShortName'].lower().replace(' ', '').replace('/', '')).encode('ASCII', 'ignore').decode('utf-8')
        if short_name not in df_dict[uf]:
            df_dict[uf][short_name] = {'Name': group_df.iloc[0]['instName'], 'Results': []}
        if result := Result.find_in_list(df_dict[uf][short_name]['Results'], year):
            result[phase] = best_rank
        else:
            df_dict[uf][short_name]['Results'].append(eval(f'Result({year}, {phase}={best_rank})'))

    return df_dict


def create_files(df):
    for uf, inst_dict in df2dict(df).items():
        institutions, uf_results = [], []
        for short_name, info in inst_dict.items():
            create_school(uf, short_name, info['Name'], info['Results'])

            institutions.append((short_name, info['Name']))
            for result in info['Results']:
                if uf_result := Result.find_in_list(uf_results, result.year):
                    for phase in PHASES:
                        if uf_result[phase] == 'null' or (result[phase] != 'null' and uf_result[phase] > result[phase]):
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


if __name__ == '__main__':
    # update_school('df', 'unb', '2022', 'Nacional', '7')
    # exit(0)
    guess_uf = quiet = True

    pattern = re.compile(r'.*\d{4}_(1aFase|Nacional|Mundial)\.csv$')
    pattern = re.compile(r'.*20(19|20|21|22)_(1aFase|Nacional|Mundial)\.csv$')
    # pattern = re.compile(r'.*20(16|17|18|19)_(1aFase|Nacional|Programadores|Mundial)\.csv$')
    pattern = re.compile(r'.*20(16|17)_(1aFase|Nacional|Mundial)\.csv$')
    pattern = re.compile(r'.*20(16|17|18|19|20|21|22)_(1aFase|Nacional|Mundial)\.csv$')
    files = [os.path.join(root, f)
             for root, dirs, files in os.walk('../reports')
             for f in files if pattern.match(f)]

    df = None
    for file in sorted(files, reverse=True):
        year, phase, contest_df = report.process(file, guess_uf, not quiet)

        if contest_df is not None:
            contest_df['Phase'] = phase if phase != '1aFase' else 'PrimeiraFase'
            contest_df['Year'] = year
            if df is None:
                df = contest_df
            else:
                df = df.append(contest_df, verify_integrity=True, ignore_index=True)

    create_files(df)
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
