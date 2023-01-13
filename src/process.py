import argparse
import html
import re
import report
import os


def _process_report_file(file, guess_uf, verbose):
    year, phase, df = report.process(file, guess_uf, verbose)
    df['Year'], df['Phase'] = year, phase
    return df[(df.role == 'CONTESTANT') & (df.teamRank > 0) & (df.teamStatus == 'ACCEPTED')]


def new_year(year):
    path, index = html.Contest.path_index(year)
    if os.path.isdir(path):
        raise ValueError(f'Diretório para o ano {year} já existe.')
    return int(year)


def process_contest(args):
    for file in args.files:
        df = _process_report_file(file, True, args.verbose)
        html.Contest.process(df)
        html.School.process(df)


def report_file(file):
    if not os.path.isfile(file):
        raise ValueError(f'"{file}" não existe!')
    phases = '|'.join(p.name for p in html.Phases)
    if not re.match(f'.*\\d{{4}}_({phases})\\.csv$', file):
        raise ValueError(f'"{file}" não é um arquivo no formato YYYY_FASE.csv!')
    return file


def process_new(args):
    path, index = html.Contest.path_index(args.year)
    html.Contest.Index.make(args.year)
    for phase in html.Phases:
        html.Contest.Phase.make(args.year, phase.name)
    if args.update_js:
        file = os.path.join('..', 'docs', 'maratona.js')
        repl = {r"year: '\d{4}'": f"year: '{args.year}'",
                r"phase: '\w+'": f"phase: ''"}
        html.file_sub(file, repl, file)


def process_report(args):
    _process_report_file(args.file, args.guess, True)


def process_reset(args):
    html.Contest.History.reset()
    html.School.reset()


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(process=lambda x: parser.print_usage())
    subparsers = parser.add_subparsers(help='Sub-comandos', dest='command')
    ###########################################################################
    contest = subparsers.add_parser('contest', help='Atualizar arquivos HTML'
                                    ' com os dados de etapa(s) da competição')
    contest.add_argument('files', nargs='*', type=report_file,
                         help='Arquivo(s) com relatório(s) do ICPC')
    contest.add_argument('-v', '--verbose', action='store_true',
                         help='Exibir detalhes do processamento')
    contest.set_defaults(process=process_contest)
    ###########################################################################
    new = subparsers.add_parser('new', help='Inicializar arquivos HTML de um'
                                ' novo ano da competição')
    new.add_argument('year', type=new_year, help='Ano da competição')
    new.add_argument('-u', '--update-js', action='store_true',
                     help='Atualizar o arquivo JS com o novo ano.')
    new.set_defaults(process=process_new)
    ###########################################################################
    report = subparsers.add_parser('report', help='Gerar relatório(s) '
                                   'referente(s) a arquivos')
    report.add_argument('file', type=report_file, help='Arquivo(s) com '
                        'relatório(s) do ICPC')
    report.add_argument('-g', '--guess', action='store_true',
                        help='Tentar adivinhar a UF da instituição')
    report.set_defaults(process=process_report)
    ###########################################################################
    reset = subparsers.add_parser('reset', help='Apagar informações/arquivos '
                                  'gerados automaticamente')
    reset.set_defaults(process=process_reset)
    ###########################################################################
    args = parser.parse_args()
    args.process(args)


if __name__ == '__main__':
    main()
