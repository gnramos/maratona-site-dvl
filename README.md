# Site da Maratona de Programação

Arquivos para divulgação das informações sobre a etapa brasileira do [ICPC](https://icpc.global/).

## src

Diretório com os arquivos de código para processamento de relatórios.

## docs

Diretório com os arquivos do site.

A criação de um novo evento é simples:
1. Duplique o diretório [template](docs/historico/template) e atualize seu nome para o ano vigente.
1. Ajustar o valor de `CURRENT_YEAR` ([aqui](docs/maratona.js)) para o novo ano.
1. Inclua o link do ano anterior na página [índice](docs/historico/index.html) do histórico.
1. Acrescente as informações da edição atual do evento aos arquivo do novo diretório.

#### Instituições

A página de cada instituição é gerada automaticamente a partir dos relatórios de resultados. Caso queira que a página da sua instituição seja atualizada com a marca própria, basta criar um [pull request](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) incluindo o arquivo. Este deve ser uma imagem no formato [png](https://pt.wikipedia.org/wiki/PNG) com nome igual ao da página da instituição (geralmente a sigla - confira na página HTML criada para sua instituição).