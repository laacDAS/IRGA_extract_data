# IRGA Extract Data 🌱📊

Um utilitário para extração e organização de dados de arquivos CSV exportados de equipamento LI-COR Infrared Gas Analyzer (IRGA), com interface gráfica amigável.

## ✨ Funcionalidades

- Interface gráfica intuitiva para seleção, visualização e remoção de arquivos.
- Processamento em lote de múltiplos arquivos CSV.
- Definição individual da chave de identificação do tratamento para cada arquivo.
- Agora é possível inserir **múltiplas chaves de tratamento** para cada arquivo, separando-as por vírgula (ex: `trat, tratamento, experimento`). O sistema buscará qualquer uma das chaves para identificar o tratamento.
- Visualização rápida: clique no nome do arquivo para abri-lo no programa padrão do sistema.
- Remoção fácil de arquivos da lista com botão "✕".
- Relatório ao final do processamento com número de linhas extraídas por arquivo.
- Acesso rápido à pasta de saída.

## 🆕 Novidade: múltiplas chaves de tratamento

Agora é possível definir **mais de uma chave de tratamento** para cada arquivo! Basta separar as chaves por vírgula no campo correspondente da interface (exemplo: `trat1,trat2,trat3`). O utilitário irá buscar e extrair os dados para todas as chaves informadas, facilitando o processamento de experimentos com múltiplos tratamentos ou repetições.

- A dica sobre múltiplas chaves aparece ao passar o mouse no campo de chave de tratamento.
- O processamento e a geração dos arquivos de saída consideram todas as chaves informadas.

## 🛠️ Instalação e requisitos

- **Python:** O projeto foi desenvolvido e testado com Python 3.11+.
- **Dependências:**
  - ttkbootstrap

### Instale o Python

Baixe e instale o Python em: [python.org/downloads](https://www.python.org/downloads/)

Durante a instalação, marque a opção **Add Python to PATH**.

### Instale as dependências

Abra o terminal na pasta do projeto e execute:

```
pip install ttkbootstrap
```

Se desejar, crie um ambiente virtual antes:

```
python -m venv venv
venv\Scripts\activate  # Windows
pip install ttkbootstrap
```

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

## 🔗 Links externos e referências
- [Support: LI-6400/XT Portable Photosynthesis System](https://www.licor.com/support/LI-6400/topics/system-description.html)
- [Support: LI-6800 Portable Photosynthesis System](https://www.licor.com/support/LI-6800/topics/matching-the-analyzers.html)
- [Python CSV Module](https://docs.python.org/3/library/csv.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)