import csv
import re
import os
from typing import List, Optional


def extrair_dados_irga_csv(arquivo_entrada: str, arquivo_saida: str, chave_trat: str | list[str] = "trat") -> int:
    """
    Extrai dados relevantes do arquivo CSV do IRGA, mantendo apenas:
    - O cabeçalho correto (linha que começa com 'Obs,HHMMSS')
    - Linhas de dados (primeira coluna é um número)
    - Linhas 'Remark=' cuja célula seguinte contenha qualquer uma das chaves_trat, associando ao próximo bloco de dados
    Salva o resultado em um novo arquivo CSV.
    A coluna 'Tratamento' armazena apenas o valor do tratamento, sem hora.

    Parâmetros:
        arquivo_entrada (str): Caminho do arquivo CSV de entrada.
        arquivo_saida (str): Caminho do arquivo CSV de saída.
        chave_trat (str | list[str]): Palavra-chave ou lista de palavras-chave para identificar o tratamento (ex: 'trat' ou ['trat', 'tr']).
    Retorna:
        int: Quantidade de linhas de dados extraídas.
    """
    dados_extraidos = []
    header = None
    tratamento_atual: Optional[str] = None
    # Permite múltiplas chaves
    if isinstance(chave_trat, str):
        chaves = [c.strip() for c in chave_trat.split(',') if c.strip()]
    else:
        chaves = [c.strip() for c in chave_trat if c.strip()]

    with open(arquivo_entrada, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # Identifica o cabeçalho correto
            if not header and row[0].strip().lower().startswith('obs'):
                header = row
                if 'Tratamento' not in header:
                    header = ['Tratamento'] + header
                continue
            # Coleta linhas Remark= com qualquer chave_trat
            if row[0].strip().lower().startswith('remark='):
                if len(row) > 1:
                    for chave in chaves:
                        idx = row[1].lower().find(chave.lower())
                        if idx != -1:
                            # Extrai o nome do tratamento a partir da chave encontrada
                            tratamento = row[1][idx:]
                            # Pega só a palavra do tratamento (até espaço, vírgula, aspas ou fim)
                            tratamento = re.split(r'[\s,\"]', tratamento)[0]
                            tratamento_atual = tratamento
                            break
                continue
            # Coleta linhas de dados (primeira coluna é número)
            if header and re.match(r'^\d+$', row[0].strip()):
                dados_extraidos.append([tratamento_atual] + row)

    if header and dados_extraidos:
        os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header)
            writer.writerows(dados_extraidos)
        return len(dados_extraidos)
    else:
        print('Nenhum dado extraído ou cabeçalho não encontrado.')
        return 0
