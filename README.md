# Site da Maratona de Programação

Arquivos para divulgação das informações sobre a etapa brasileira do [ICPC](https://icpc.global/).

## src

Diretório com os arquivos de código para processamento de relatórios.

## www

Diretório com os arquivos do site.

A criação de um novo evento é simples:
1. Duplique o diretório [template](www/historico/template) e atualize seu nome para o ano vigente.
1. Ajustar o valor de `CURRENT_YEAR` ([aqui](www/maratona.js)) para o novo ano.
1. Inclua o link do ano anterior na página [índice](www/historico/index.html) do histórico.
1. Acrescente as informações da edição atual do evento aos arquivo do novo diretório.

#### Instituições

Caso queira que a página da sua instituição seja atualizada com a marca própria e o link para um site externo, basta criar um [pull request](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) com estas atualizações. O nome do arquivo da imagem deve ser igual ao da página da instituição (geralmente a sigla).