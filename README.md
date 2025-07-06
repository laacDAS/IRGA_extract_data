# IRGA Extract Data 🌱📊

Um utilitário para extração e organização de dados de arquivos CSV exportados de equipamento LI-COR Infrared Gas Analyzer (IRGA), com interface gráfica amigável.

## ✨ Funcionalidades

- Interface gráfica intuitiva para seleção, visualização e remoção de arquivos.
- Processamento em lote de múltiplos arquivos CSV.
- Definição individual da chave de identificação do tratamento para cada arquivo.
- Visualização rápida: clique no nome do arquivo para abri-lo no programa padrão do sistema.
- Remoção fácil de arquivos da lista com botão "✕".
- Relatório ao final do processamento com número de linhas extraídas por arquivo.
- Acesso rápido à pasta de saída.

## 🚀 Como usar

1️⃣ **Salve os arquivos exportados do IRGA** na pasta `dados`. O arquivo de saída será salvo automaticamente na pasta `saida` após o processamento.

2️⃣ **Os arquivos de entrada devem ser em formato CSV**:

- Codificação: UTF-8
- Delimitador de campo: vírgula (,)
- Delimitador de texto: aspas duplas ("")

3️⃣ **Execute o `main.py`** para iniciar a interface gráfica ou clique duas vezes em **open_app.vbs**:

- Clique em **Selecionar Arquivos** para adicionar um ou mais arquivos CSV.
- Para cada arquivo, defina a chave de identificação do tratamento (ex: `trat`).
- Clique no nome do arquivo para abri-lo diretamente.
- Use o botão vermelho **✕** para remover arquivos da lista, se necessário.

4️⃣ Clique em **Processar** para extrair os dados. Ao final, será exibido um relatório com o número de arquivos processados e linhas extraídas de cada um.

5️⃣ Use o botão **Abrir pasta de saída** para acessar rapidamente os arquivos processados.

## 💡 Sobre o projeto

Este projeto foi criado para facilitar a rotina de pesquisadores e técnicos que trabalham com dados de trocas gasosas em plantas, especialmente o modelo da LI-COR, automatizando a limpeza e organização dos arquivos gerados pelo IRGA. A interface foi pensada para ser simples e eficiente.

- Código aberto e personalizável.
- Compatível com Windows.

## Links externos e referências
- [Support: LI-6400/XT Portable Photosynthesis System](https://www.licor.com/support/LI-6400/topics/system-description.html)
- [Support: LI-6800 Portable Photosynthesis System](https://www.licor.com/support/LI-6800/topics/matching-the-analyzers.html)
- [Python CSV Module](https://docs.python.org/3/library/csv.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)