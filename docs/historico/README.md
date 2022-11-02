# Eventos

Todo evento é baseado em fases que ocorrem durante um ano. A padronização dos arquivos e da estrutura facilita a criação/manutenção de conteúdo.

A estrutura de diretório definida é:
```
YYYY
  +- index.html
  +- FaseZero
  +- 1aFase
  +- Nacional
  +- SummerSchool
  +- Mundial
```

Ela é replicada para cada ano (`YYYY`), e as informações organizadas em subdiretórios, um para cada fase. O arquivo `index.html` mostra o poster do evento e um índice para cada fase.

## Fase Zero


## 1a Fase

A estrutura de diretório definida é:
```
1aFase
  +- contest
  |    +- clarifications.html
  |    +- info_maratona.pdf
  |    +- maratona.pdf
  |    +- packages.tar.gz
  |    +- runs.html
  |    +- score.html
  |    `- statistics.html
  `- index.html
```

A página  apresenta, a princípio, 3 blocos de informações distintos. Mais informações podem ser acrescentadas se necessário (seguindo o padrão de formatação).

### Organização
As informações sobre a organização do evento.

### Prova
São fornecidos os links para os arquivos utilizados, que devem *necessariamente* ser como previsto na estrutura:
* Folha de Informações em `info_maratona.pdf`,
* Problemas da Prova em `maratona.pdf`, e
* Entradas e Saídas em `packages.tar.gz`.

### Resultados
São fornecidos os links para os arquivos utilizados, que devem *necessariamente* ser como previsto na estrutura:
* Placar final em `score.html`,
* Lista de submissões em `runs.html`,
* Lista de perguntas em `clarifications.html`, e
* Estatísticas em `statistic.html`.

### index.html
O arquivo `index.html` determina o conteúdo. A formatação é praticamente toda definida automaticamente, via CSS e javascript, sendo necessário apenas definir alguns conteúdos como HTML. Especificamente:
* `initial_info`: as informações a serem apresentadas no topo da página.
* `organization`: as informações a serem apresentadas no bloco de "organização", geralmente a listagem dos envolvidos na organização do evento.
* contest_problems: a lista dos nomes dos problemas (e seus autores), na mesma ordem que aparecem na prova.
* `results [limiar_ok + supersedes]`: os resultados dos times classificados em cada sede.

## Final Brasileira

A estrutura do diretório é:
```
Nacional
  +- contest
  |    +- clarifications_arquivos
  |    +- runs_arquivos
  |    +- statistics_arquivos
  |    +- score-admin_arquivos
  |    +- clarifications.html
  |    +- info_maratona.pdf
  |    +- maratona.pdf
  |    +- packages.tar.gz
  |    +- runs.html
  |    +- score.html
  |    `- statistics.html
  +- img
  |    +- poster.jpg
  |    +- teamX.webp  // 1 <= X <= 12 (total de medalhistas)
  +- warmup
  |    +- info_maratona.pdf
  |    +- maratona.pdf
  |    +- packages.tar.gz
  |    `- slides.pdf
  `- index.html
```

## Summer School

## Final Mundial
