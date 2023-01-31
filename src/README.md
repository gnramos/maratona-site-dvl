# Processamento

O processamento do(s) relatório(s) é feito por scripts em Python 3 (e [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)). O uso é simples:

```bash
python3 process.py -h
```

## `contest`

O resultado de processar um `contest` é a criação/atualização dos dados de um arquivo do relatório do ICPC, inclusive no histórico e no acumulado da UF *se o resultado for melhor que o registrado* (caso a instituição que tinha o melhor resultado da competição registrado tenha este valor alterado para um resultado pior, o histórico da UF ficará desatualizado). O uso do comando `new` é restrito a criação de um novo registro de competição (anual) para não sobrescrever arquivos existentes.

## `new`

Crie a estrutura de diretórios para um ano. Se preferir não usar a atualização automática (`-u`), é necessário atualizar os valores de `CURRENT_YEAR` e `CURRENT_PHASE` em [maratona.js](../docs/maratona.js) manualmente para que os links funcionem corretamente.

Atualize a página [inscricoes](../docs/inscricoes.html). Atenção pra garantir a funcionalidade de links como o para o "Manual do Diretor" ou formulários de inscrição para Fase 0 ou Café-com-leite.

Atualize a lista de sedes (`sites`) na página [eventos](../docs/eventos/index.html) com o local da sede do ano anterior.

## `report`

Processa um relatório do [ICPC](http://icpc.global/). O arquivo deve ser nomeado como `YYYY_FASE.csv`, indicando o ano do evento e a fase associadas aos dados, e deve ser exportado pelo próprio dashboard do site, contendo os seguintes 11 dados: *role*, *username*, *firstName*, *lastName*, *sex*, *teamName*, *teamStatus*, *teamRank*, *instName*, *instShortName*, *siteName*.

## `reset`

Apaga *todos* os resultados de eventos. Isso implica o histórico de participações e os históricos de todas as instituições em cada UF. As páginas específicas das fases por ano *não são alteradas*.