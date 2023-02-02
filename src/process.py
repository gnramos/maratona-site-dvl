import argparse
import html
import re
import report
import os


def _new_year(year):
    path, index = html.Event.path_index(year)
    if os.path.isdir(path):
        raise ValueError(f'Diretório para o ano {year} já existe.')
    return int(year)


def _process_event(args):
    for file in sorted(args.files):
        df = _process_report_file(file, True, args.verbose)
        if df is not None:
            html.Event.process(df)
            html.School.process(df)


def _process_new(args):
    path, index = html.Event.path_index(args.year)
    html.Event.create(args.year)
    if args.current:
        file = os.path.join('..', 'docs', 'maratona.js')
        repl = {r"year: '\d{4}'": f"year: '{args.year}'",
                r"phase: '\w+'": "phase: ''"}
        html.file_sub(file, repl, file, 1)


def _process_report(args):
    _process_report_file(args.file, args.guess, True)


def _process_report_file(file, guess_uf, verbose):
    df = report.process(file, guess_uf, verbose)
    if df is None or df.empty:
        return None
    return df[(df.role == 'CONTESTANT') & (df.teamRank > 0) & (df.teamStatus == 'ACCEPTED')]


def _process_reset(args):
    html.Event.reset_index()
    html.School.reset()


def _report_file(file):
    if not os.path.isfile(file):
        raise ValueError(f'"{file}" não existe!')
    phases = '|'.join(p.name for p in html.Event.Phases)
    if not re.match(f'.*\\d{{4}}_({phases})\\.csv$', file):
        raise ValueError(f'"{file}" não é um arquivo no formato YYYY_FASE.csv!')
    return file


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(process=lambda x: parser.print_usage())
    subparsers = parser.add_subparsers(help='Sub-comandos', dest='command')
    ###########################################################################
    event = subparsers.add_parser('event', help='Atualizar arquivos HTML'
                                  ' com os dados de etapa(s) da competição')
    event.add_argument('files', nargs='*', type=_report_file,
                       help='Arquivo(s) com relatório(s) do ICPC')
    event.add_argument('-v', '--verbose', action='store_true',
                       help='Exibir detalhes do processamento')
    event.set_defaults(process=_process_event)
    ###########################################################################
    new = subparsers.add_parser('new', help='Inicializar arquivos HTML de um'
                                ' novo ano da competição')
    new.add_argument('year', type=_new_year, help='Ano da competição')
    new.add_argument('-c', '--current', action='store_true',
                     help='Definir ano como o atual no arquivo JS.')
    new.set_defaults(process=_process_new)
    ###########################################################################
    report = subparsers.add_parser('report', help='Gerar relatório(s) '
                                   'referente(s) a arquivos')
    report.add_argument('file', type=_report_file, help='Arquivo(s) com '
                        'relatório(s) do ICPC')
    report.add_argument('-g', '--guess', action='store_true',
                        help='Tentar adivinhar a UF da instituição')
    report.set_defaults(process=_process_report)
    ###########################################################################
    reset = subparsers.add_parser('reset', help='Apagar informações/arquivos '
                                  'gerados automaticamente')
    reset.set_defaults(process=_process_reset)
    ###########################################################################
    args = parser.parse_args()
    args.process(args)


if __name__ == '__main__':
    main()
