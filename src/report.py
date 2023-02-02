from collections import namedtuple
import os
import pandas as pd
import random
import re

# Arquivo com as informações consideradas corretas para cada instituição.
INSTITUTIONS_CSV = 'institutions.csv'
Institution = namedtuple('Institution', 'UF short full')

# Arquivo com possíveis formas de escrita dao nome das instituições.
ALIASES_CSV = 'aliases.csv'
# "Constantes" globais para armazenar informações dos arquivos CSV.
ALIASES, INSTITUTIONS = {}, {}

# Valores para região/sede usados na etapa "Nacional".
NATIONAL_REGION, NATIONAL_UF = 'Brasil', 'BR'

# Mapeamento das relações geográficas.
REGION_UF = {'Centro-Oeste': ['DF', 'GO', 'MS', 'MT'],
             'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
             'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
             'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
             'Sul': ['PR', 'RS', 'SC']}

STATE_UF = {'Acre': 'AC', 'Alagoas': 'AL', 'Amazonas': 'AM', 'Amapá': 'AP',
            'Bahia': 'BA',
            'Ceará': 'CE',
            'Distrito Federal': 'DF',
            'Espírito Santo': 'ES',
            'Goiás': 'GO',
            'Maranhão': 'MA', 'Minas Gerais': 'MG',
            'Mato Grosso do Sul': 'MS', 'Mato Grosso': 'MT',
            'Pará': 'PA', 'Paraíba': 'PB', 'Pernambuco': 'PE', 'Piauí': 'PI',
            'Paraná': 'PR',
            'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN',
            'Rondônia': 'RO', 'Roraima': 'RR', 'Rio Grande do Sul': 'RS',
            'Santa Catarina': 'SC', 'Sergipe': 'SE', 'São Paulo': 'SP',
            'Tocantins': 'TO'}

SHORT = 'instShortName'  # melhorar a legibilidade do código
CONTESTANTS_PER_TEAM = 3  # número mágico
###############################################################################
# Funções auxiliares


def normalize(text, remove_spaces=True):
    import unicodedata

    if remove_spaces:
        text = re.sub(r'[^\w]', '', text.lower())
    else:
        text = ' '.join(re.sub(r'[^\w]', '', p) for p in text.lower().split())

    return unicodedata.normalize('NFD', text).encode('ASCII', 'ignore').decode('utf-8')


# Variações nos nomes de estados para lidar com falta de padronização da
# escrita.
ALIAS_STATE = {normalize(s): s for s in STATE_UF}
UF_REGION = {uf: region for region, ufs in REGION_UF.items() for uf in ufs}


def _alias(institution):
    return ALIASES.get(normalize(institution), institution)


def _capitalize(string):
    return ' '.join(word.capitalize() for word in string.split())


def _check_data(df):
    problems = []

    missing_short = list(df[df[SHORT].isna()]['instName'].unique())
    if missing_short:
        problem = 'Inclua o "short name" das seguintes ' \
                  f'instituições no arquivo "{INSTITUTIONS_CSV}".'
        problems.append((problem, sorted(missing_short)))

    uf_df = df[df['UF'] == NATIONAL_UF]
    missing_UFs = [f'{Guess.uf_from_institution(g[1])},{g[0]},{g[1]}'
                   for g, _ in uf_df.groupby(by=[SHORT, 'instName'])]

    if missing_UFs:
        problem = ('É preciso incluir as seguintes instituições no '
                   f'arquivo "{INSTITUTIONS_CSV}". A UF é apenas uma '
                   'sugestão, confirme a informação manualmente.')
        problems.append((problem, sorted(missing_UFs)))

    # Ajustando a UF, a região é automaticamente corrigida (_preprocess).
    return problems


def _remove_uf_from_site(site):
    for sep in ('-', ','):
        site = sep.join(p for p in site.split(sep) if p.strip() not in UF_REGION)
    return site.strip()


class Get:
    @staticmethod
    def uf_from_institution(institution):
        if info := INSTITUTIONS.get(normalize(institution), False):
            return info.UF
        return NATIONAL_UF

    @staticmethod
    def short_name_from_full(institution, known_short):
        if info := INSTITUTIONS.get(normalize(institution), False):
            if info.short:
                return info.short
        return known_short

    @staticmethod
    def region_from_uf(uf):
        return UF_REGION.get(uf, NATIONAL_REGION)

    @staticmethod
    def uf_from_site(site):
        parts = site.upper().split()
        for uf in UF_REGION:
            if uf in parts:
                return uf

        site = normalize(site)
        for s, state in ALIAS_STATE.items():
            if s in site:
                return STATE_UF[state]
        return NATIONAL_UF

    @staticmethod
    def uf_from_institution(uf_or_statename):
        if uf_or_statename in UF_REGION:
            return uf_or_statename

        if uf_or_statename in ALIAS_STATE:
            return STATE_UF[ALIAS_STATE[uf_or_statename]]

        n_institution = normalize(_alias(uf_or_statename))
        if info := INSTITUTIONS.get(n_institution, False):
            return info.UF
        return NATIONAL_UF


class Guess:
    @staticmethod
    def region_from_full(full_name):
        return UF_REGION.get(Guess.uf_from_full(full_name), NATIONAL_REGION)

    @staticmethod
    def uf_from_institution(full_name, site=''):
        if (uf := Get.uf_from_institution(full_name)) != NATIONAL_UF:
            return uf

        for state, uf in STATE_UF.items():
            if (re.search(f'\\b{state}\\b', full_name, re.IGNORECASE) or
                re.search(f'\\b{uf}\\b', full_name, re.IGNORECASE) or
                re.search(f'\\b{normalize(state, remove_spaces=False)}\\b', normalize(full_name, remove_spaces=False), re.IGNORECASE) or
                re.search(f'\\bUF{uf}]\\b', full_name, re.IGNORECASE) or
                re.search(f'\\b{uf}\\b', site, re.IGNORECASE)):
                return uf

        return NATIONAL_UF


def _hash(text):
    text = [c for c in re.sub(r'[\W_]', '', text.lower())]
    random.seed(sum(ord(text[i]) for i in range(0, len(text), 2)))
    random.shuffle(text)
    return ''.join(text)


def _log(messages, level=0):
    if isinstance(messages, str):
        messages = [messages]

    for msg in messages:
        print(f'{"  " * level} {msg}')


def _preprocess(df, guess_uf=False, verbose=True):
    # df['username'] = df['username'].apply(_hash)
    df['instName'] = df['instName'].apply(_alias)

    for i, row in df.iterrows():
        df.at[i, SHORT] = Get.short_name_from_full(row['instName'], row[SHORT])

    # for i, row in df[df[SHORT].isna()].iterrows():
    #     df.at[i, SHORT] = Get.short_name_from_full(row['instName'])

    df['UF'] = df['siteName'].apply(Get.uf_from_site)
    if guess_uf:
        for i, row in df[df['UF'] == NATIONAL_UF].iterrows():
            df.at[i, 'UF'] = Guess.uf_from_institution(row['instName'], row['siteName'])

    df['Region'] = [UF_REGION.get(uf, NATIONAL_REGION) for uf in df['UF']]
    df['siteName'] = df['siteName'].apply(_remove_uf_from_site)
    df['FullName'] = (df['firstName'] + ' ' + df['lastName']).apply(_capitalize)
    df['teamRank'] = df['teamRank'].fillna(df['teamRank'].max())
    df['SiteRank'] = df['teamRank']

    # Incluir rank da Sede.
    ranks = df[df['teamRank'] > 0].sort_values(by=['Region', 'siteName', 'teamRank'])
    for _, group_df in ranks.groupby(by=['Region', 'siteName']):
        for site_rank, (x, team_rank) in enumerate(group_df.groupby('teamRank')):
            df.at[team_rank.index, 'SiteRank'] = site_rank + 1

    df = df.drop(['firstName', 'lastName'], axis=1)
    return df


def _read_csv(file, verbose=True):
    df = pd.read_csv(file, encoding='utf-8')

    if verbose:
        _log(f'{df.shape[0]} registros.')

    df = df.drop(df[df['teamStatus'] != 'ACCEPTED'].index)
    if verbose:
        _log(f'{df.shape[0]} registros aceitos.')

    return df


class Statistics:
    @staticmethod
    def show(df):
        teams = df['teamName'].unique()
        contestants = df[df['role'] == 'CONTESTANT']
        female_contestants = contestants[contestants['sex'] == 'FEMALE']
        all_female_teams = female_contestants[
            female_contestants.groupby('teamName')[
                'teamName'].transform('count') == CONTESTANTS_PER_TEAM]['teamName'].unique()
        coaches = df[df['role'] == 'COACH']
        student_coaches = df[df['role'] == 'STUDENT_COACH']

        _log(f'{len(df["instName"].unique()):4d} instituições.')
        _log(f'{len(coaches.groupby(["FullName"]).count().index):4d} coaches')
        _log(f'{len(student_coaches.groupby(["FullName"]).count().index):4d} '
             'student-coaches')
        _log(f'{contestants.shape[0]:4d} competidores em {len(teams)} times.')
        _log(f'{contestants.shape[0] - female_contestants.shape[0]:4d} alunOs em '
             f'{len(teams) - all_female_teams.shape[0]} times.')
        _log(f'{female_contestants.shape[0]:4d} alunA(s) em '
             f'{len(female_contestants["teamName"].unique())} time(s) ('
             f'{100 * female_contestants.shape[0] / contestants.shape[0]:.0f}% '
             'dos competidores)')
        if all_female_teams.size > 0:
            _log(f'{len(all_female_teams):4d} time(s) composto(s) apenas por '
                 f'mulheres ({100 * len(all_female_teams) / len(teams):.1f}% '
                 'dos times)')

    @staticmethod
    def region_best(df):
        _log('Campeões Regionais')
        for _, group_df in df.sort_values(['Region', 'teamRank']).groupby('Region'):
            _log(f'{group_df.iloc[0]["Region"]} > {group_df.iloc[0]["teamName"]}', 1)

    @staticmethod
    def site_best(df):
        _log('Campeões por Sede')
        GROUPS = ['Region', 'UF', 'siteName'] if df['Phase'].iloc[0] == 'Primeira' else ['siteName']
        sites = df.sort_values(by=['siteName', 'teamRank'])
        for _, group_df in sites.groupby(by=GROUPS):
            row = group_df.iloc[0]
            links = ' > '.join(row[group] for group in GROUPS)
            _log(f'{links} > {row["teamName"]}', 1)


# Função principal.
def process(file, guess_uf=False, verbose=True):
    """Processa o arquivo, gerando um DataFrame com as informações.

    Retorna um DataFrame com as informações do arquivo.
    """

    if verbose:
        _log(f'Processando "{file}"...')

    _, tail = os.path.split(file)
    name, _ = os.path.splitext(tail)
    year, phase = name.split('_')
    _log(f'{year} - {phase}')

    df = _read_csv(file, verbose)
    df['Year'], df['Phase'] = year, phase
    df = _preprocess(df, guess_uf, verbose)

    if problems := _check_data(df):
        print("Pendências identificadas!")
        for description, details in problems:
            _log(f'- {description}', 1)
            for detail in details:
                _log(f'* {detail}', 2)

        if input("Continuar? (S/N) ") not in "sS":
            return None

    if verbose:
        Statistics.show(df)
        Statistics.region_best(df)
        Statistics.site_best(df)

    return df
###############################################################################


# Carregar informações dos arquivos.
with open(ALIASES_CSV) as file:
    next(file)  # Remove header.
    for line in file:
        alias, name = line.split(',', 1)
        ALIASES[alias] = name.rstrip()

with open(INSTITUTIONS_CSV) as file:
    next(file)  # Remove header.
    for line in file:
        uf, short, full = line.rstrip().split(',', 2)
        institution = Institution(uf, short, full)
        INSTITUTIONS[normalize(full)] = institution
        if short:
            INSTITUTIONS[normalize(short)] = institution
