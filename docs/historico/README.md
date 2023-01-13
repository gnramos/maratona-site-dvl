# Eventos

Todo evento é baseado em fases que ocorrem durante um ano. A padronização dos arquivos e da estrutura facilita a criação/manutenção de conteúdo.

A estrutura de diretório definida é:
```
YYYY
  +- index.html
  +- Zero
  +- Primeira
  +- Nacional
  `- Mundial
```

Ela é replicada para cada ano (`YYYY`), e as informações organizadas em subdiretórios, um para cada fase.

## Contest Info

Cada fase implica a aplicação de uma prova, cujas informações pertinentes devem estar contida no diretórios `contest` com *exatamente* os arquivos definidos a seguir:
```
+- contest
|    +- clarifications.html (html com as informações dos esclarecimentos solicitados - BOCA)
|    +- editorial.pdf       (tutorial para a solução dos problemas - opcional)
|    +- info_maratona.pdf   (folha de informações da prova)
|    +- maratona.pdf        (folha de problemas da prova)
|    +- packages.tar.gz     (arquivos de entrada/saída para os problemas)
|    +- runs.html           (html com as informações das submissões realizadas - BOCA)
|    +- score.html          (html com o placar final do evento - BOCA)
|    `- statistics.html     (html com as estatísticas do evento - BOCA)
```

## Fase Zero


## 1a Fase

A estrutura de diretório definida é:
```
Primeira
  +- contest
  +- warmup
  +- index.html
  `- manual_diretor.pdf
```

A página apresenta, a princípio, 3 blocos de informações distintos. Mais informações podem ser acrescentadas se necessário (seguindo o padrão de formatação).

### Organização

As informações sobre a organização do evento.

### Prova

Detalhes sobre o evento, com a listagem dos problemas e com arquivos associados à prova no diretório `contest`, que devem *necessariamente* ser nomeados como previsto na estrutura:
* folha de Informações em `info_maratona.pdf`,
* problemas da Prova em `maratona.pdf`, e
* entradas e Saídas em `packages.tar.gz`.

### Resultados

Detalhes sobre o resultado evento, com a listagem dos problemas e com arquivos associados à prova no diretório `contest`, que devem *necessariamente* ser nomeados como previsto na estrutura:
* página web com o placar final em `score.html`,
* página web com as submissões em `runs.html`,
* página web com as _clarifications_ em `clarifications.html`, e
* página web com as estatísticas do evento em `statistics.html`.

### index.html

O arquivo `index.html` determina o conteúdo. A formatação é praticamente toda definida automaticamente, via CSS e javascript, sendo necessário apenas definir alguns conteúdos como HTML. Especificamente:
* `pageStart`: as informações a serem apresentadas no topo da página.
* `organization`: as informações a serem apresentadas no bloco de "organização", geralmente a listagem dos envolvidos na organização do evento.
* `contestProblems`: a lista dos nomes dos problemas (e seus autores), na mesma ordem que aparecem na prova.
* `results`: os resultados dos times classificados em cada sede.

## Final Brasileira

A estrutura do diretório é:
```
Nacional
  +- contest
  |    +- clarifications.html
  |    +- info_maratona.pdf
  |    +- maratona.pdf
  |    +- packages.tar.gz
  |    +- runs.html
  |    +- score.html
  |    `- statistics.html
  +- img
  |    +- poster_low.png
  |    +- poster_high.png
  |    +- teamX.webp  // 1 <= X <= {9, 12} (total de medalhistas)
  +- warmup
  |    +- info_maratona.pdf
  |    +- maratona.pdf
  |    +- packages.tar.gz
  |    `- slides.pdf
  `- index.html
```

A página apresenta, a princípio, 6 blocos de informações distintos. Mais informações podem ser acrescentadas se necessário (seguindo o padrão de formatação).

### Fotos

Carrossel com imagens do evento.

### Patrocinadores

Informações sobre os patrocinadores.

### Organização

As informações sobre a organização do evento.

### Warm Up

Detalhes sobre o Warm Up, com a listagem dos problemas e com arquivos associados à prova no diretório `warmup`, que devem *necessariamente* ser nomeados como previsto na estrutura:* arquivo com os slides apresentados na abertura do evento em `slides.pdf`,
* folha de Informações em `info_maratona.pdf`,
* problemas da Prova em `maratona.pdf`, e
* entradas e Saídas em `packages.tar.gz`.

### Prova

Detalhes sobre o evento, com a listagem dos problemas e com arquivos associados à prova no diretório `contest`, que devem *necessariamente* ser nomeados como previsto na estrutura:
* folha de Informações em `info_maratona.pdf`,
* problemas da Prova em `maratona.pdf`, e
* entradas e Saídas em `packages.tar.gz`.

### Resultados

Detalhes sobre o resultado evento, com a listagem dos problemas e com arquivos associados à prova no diretório `contest`, que devem *necessariamente* ser nomeados como previsto na estrutura:
* página web com o placar final em `score.html`,
* página web com as submissões em `runs.html`,
* página web com as _clarifications_ em `clarifications.html`, e
* página web com as estatísticas do evento em `statistics.html`.

Os times medalhistas devem ter fotos no formato `img/teamX.webp`, onde `X` indica o ranking de cada time.

### Outros

O diretório `img` contém as imagens do evento. O arquivo `img/poster_low.png` é de menor resolução para gerar a página web, já o `img/poster_high.png` serve para download e impressão do poster do evento.

## Final Mundial
