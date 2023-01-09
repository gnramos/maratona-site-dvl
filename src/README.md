# Processamento

O processamento do(s) relatório(s) é feito por scripts em Python 3 (e [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)). O uso é simples:

```bash
python3 process.py -h
```

O resultado de processar um `contest` é a criação/atualização dos dados de um arquivo com o relatório do ICPC, inclusive no histórico e no acumulado da UF *se o resultado for melhor que o registrado* (caso a instituição que tinha o melhor resultado da competição registrado tenha este valor alterado para um resultado pior, o histórico da UF ficará desatualizado). O uso do comando `new` é restrito a criação de um novo registro de competição (anual) para não sobrescrever arquivos existentes.