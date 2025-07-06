import csv
import re
from typing import List, Optional
import os


def extrair_dados_irga_csv(arquivo_entrada: str, arquivo_saida: str, chave_trat: str = "trat") -> int:
    """
    Extrai dados relevantes do arquivo CSV do IRGA, mantendo apenas:
    - O cabeçalho correto (linha que começa com 'Obs,HHMMSS')
    - Linhas de dados (primeira coluna é um número)
    - Linhas 'Remark=' cuja célula seguinte contenha a chave_trat, associando ao próximo bloco de dados
    Salva o resultado em um novo arquivo CSV.
    A coluna 'Tratamento' armazena apenas o valor do tratamento, sem hora.

    Parâmetros:
        arquivo_entrada (str): Caminho do arquivo CSV de entrada.
        arquivo_saida (str): Caminho do arquivo CSV de saída.
        chave_trat (str): Palavra-chave para identificar o tratamento (ex: 'trat').
    Retorna:
        int: Quantidade de linhas de dados extraídas.
    """
    dados_extraidos = []
    header = None
    tratamento_atual: Optional[str] = None
    # Regex para encontrar a chave_trat e capturar o restante
    pattern_remark_trat = re.compile(
        rf'{re.escape(chave_trat)}[\w\d]+', re.IGNORECASE)

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
            # Coleta linhas Remark= com chave_trat
            if row[0].strip().lower().startswith('remark='):
                if len(row) > 1:
                    match = pattern_remark_trat.search(row[1])
                    if match:
                        tratamento_atual = match.group(0)
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
