import argparse
import html
import re
import report
import os


def valid_only(args):
    phases = '|'.join(p for p in html.PHASES)
    pattern = re.compile(f'.*\\d{{4}}_({phases})\\.csv$')
    args.files = [file
                  for file in args.files
                  if pattern.match(file) and os.path.isfile(file)]


def parse_html(args):
    df = None
    for file in sorted(args.files, reverse=True):
        # Ordem inversa pois assume-se que dados mais recentes sejam mais
        # completos/acurados.
        year, phase, contest = report.process(file, args.guess, not args.quiet)
        contest['Year'], contest['Phase'] = year, phase

        if df is None:
            df = contest
        else:
            df = df.append(contest, verify_integrity=True, ignore_index=True)

    df = df[(df.role == 'CONTESTANT') & (df.teamRank > 0) & (df.teamStatus == 'ACCEPTED')]

    html.Schools.schools(df)
    html.History.contests(df)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*',
                        help='Arquivo(s) com relatório(s) do ICPC')
    parser.add_argument('-g', '--guess', action='store_false',
                        help='Tentar adivinhar a UF da instituição')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Exibir os resultados do processo')
    parser.add_argument('--html', action='store_true',
                        help='Gerar todos os arquivos HTML')

    args, unknown = parser.parse_known_args()
    valid_only(args)
    parse_html(args)
    # args.func(args)

# import argparse
# import re
# from maratona import contest, report, participation


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('files', type=str, nargs='*',
#                         help='Arquivo(s) com relatório(s) do ICPC a processar.')
#     parser.add_argument('-g', '--guess-uf', action='store_true',
#                         help='Tentar adivinhar a UF da instituição.')
#     parser.add_argument('-e', '--contestos', action='store_true',
#                         help='Processa o(s) contesto(s).')
#     parser.add_argument('-p', '--participacoes', action='store_true',
#                         help='Processa o histórico de participações.')
#     parser.add_argument('-q', '--quiet', action='store_true',
#                         help='Não mostrar as mensagens informativas.')
#     parser.add_argument('-o', '--overwrite', action='store_true',
#                         help='Sobrescrever arquivos.')
#     args = parser.parse_args()

#     pattern = re.compile(r'.*\d{4}_(Primeira|Nacional)\.csv')
#     files = [f for f in args.files if pattern.match(f)]

#     df_part = None
#     for file in sorted(files, reverse=True):
#         # Ordem inversa pois assume-se que dados mais recentes sejam mais
#         # completos/acurados.
#         year, phase, df = report.process(file, args.guess_uf, not args.quiet)

#         if df is not None:
#             if args.contestos:
#                 contest.to_file(year, phase, df, args.overwrite)
#                 contest.load_js_in_html(year, phase)

#             if args.participacoes:
#                 df['Phase'] = phase
#                 df['Year'] = year
#                 if df_part is None:
#                     df_part = df
#                 else:
#                     df_part = df_part.append(df, verify_integrity=True,
#                                              ignore_index=True)

#     if args.participacoes:
#         if not args.quiet:
#             print('Processando as participações...')
#         participation.to_file(df_part)


if __name__ == '__main__':
    main()