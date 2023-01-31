# Site da Maratona de Programação

Arquivos para divulgação das informações sobre a etapa brasileira do [ICPC](https://icpc.global/).

## `src`

Diretório com os arquivos de código para processamento de relatórios.

## `docs`

Diretório com os arquivos do site.

A criação de um novo evento é simples, basta aplicar com o script em [src](src) e preencher os arquivos gerados com as informações do evento (e, talvez, ajustar os links da página de índice).

### Histórico de Eventos

Os arquivos referentes a um evento ficam no diretório [eventos](docs/eventos), sendo organizados em subdiretórios `ano/fase`. O ano é no formato YYYY, e fase é uma das opções `Zero`, `Primeira`, `Nacional` e `Mundial`. Arquivos auxiliares para cada fase devem ser colocados em seus respectivos subdiretórios.

### Escolas

Os arquivos referentes a uma escola ficam no diretório [escolas](docs/escolas), sendo organizados em subdiretórios `região/uf`. Cada escola tem sua própria página, nomeada conforme a sigla da instituição (normalizada).

A página de cada instituição é gerada automaticamente a partir dos relatórios de resultados. Caso queira que a página da sua instituição seja atualizada com a marca própria, basta criar um [pull request](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) incluindo o arquivo. Este deve ser uma imagem no formato [png](https://pt.wikipedia.org/wiki/PNG) com nome igual ao da página da instituição (geralmente a sigla - confira na página HTML criada para sua instituição).