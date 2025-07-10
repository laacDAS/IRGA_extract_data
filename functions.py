import csv
import re
import os
from typing import List, Optional


def extrair_dados_irga(arquivo_entrada: str, arquivo_saida: str, chave_trat: str | list[str] = "trat", colunas: list[str] = None) -> int:
    """
    Extrai dados relevantes de arquivos CSV do IRGA, mantendo apenas:
    - O cabeçalho correto (linha que começa com 'Obs,HHMMSS')
    - Linhas de dados (primeira coluna é um número)
    - Linhas 'Remark=' cuja célula seguinte contenha qualquer uma das chaves_trat, associando ao próximo bloco de dados
    Permite selecionar quais colunas manter no arquivo de saída.
    Salva o resultado em um novo arquivo CSV.
    A coluna 'Tratamento' armazena apenas o valor do tratamento, sem hora.

    Parâmetros:
        arquivo_entrada (str): Caminho do arquivo de entrada (csv).
        arquivo_saida (str): Caminho do arquivo CSV de saída.
        chave_trat (str | list[str]): Palavra-chave ou lista de palavras-chave para identificar o tratamento (ex: 'trat' ou ['trat', 'tr']).
        colunas (list[str], opcional): Lista de nomes de colunas a manter no arquivo de saída. Se None, mantém todas.
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

    linhas = []
    with open(arquivo_entrada, encoding='utf-8') as f:
        reader = csv.reader(f)
        linhas = list(reader)

    indices_colunas = None
    for row in linhas:
        if not row:
            continue
        # Identifica o cabeçalho correto
        if not header and row[0].strip().lower().startswith('obs'):
            header = row
            if 'Tratamento' not in header:
                header = ['Tratamento'] + header
                row = ['Tratamento'] + row
            # Seleciona colunas
            if colunas:
                indices_colunas = [
                    i for i, col in enumerate(row) if col in colunas]
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
            linha = [tratamento_atual] + row
            if indices_colunas:
                linha = [linha[i]
                         for i in [0] + [j+1 for j in indices_colunas if j != 0]]
            dados_extraidos.append(linha)

    if header and dados_extraidos:
        os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            if indices_colunas:
                header_saida = [header[0]] + [header[i]
                                              for i in indices_colunas if i != 0]
                writer.writerow(header_saida)
            else:
                writer.writerow(header)
            writer.writerows(dados_extraidos)
        return len(dados_extraidos)
    else:
        print('Nenhum dado extraído ou cabeçalho não encontrado.')
        return 0
