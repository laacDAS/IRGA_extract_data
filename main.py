import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from functions import extrair_dados_irga_csv
import subprocess
import tkinter as tk


def abrir_saida(saida_path):
    if os.name == 'nt':
        os.startfile(saida_path)
    else:
        subprocess.Popen(['xdg-open', saida_path])


def abrir_arquivo_csv(caminho):
    if os.name == 'nt':
        os.startfile(caminho)
    else:
        subprocess.Popen(['xdg-open', caminho])


class ExtratorApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Extrator de Dados IRGA")
        self.geometry("700x440")
        self.minsize(520, 320)
        self._create_main_interface()
        self.update_idletasks()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_main_interface(self):
        frame = tb.Frame(self, padding=18)
        frame.pack(fill=tb.BOTH, expand=True)
        self.arquivos = []
        self.entries = []
        self.labels = []
        # Botão de selecionar arquivos no topo
        btn_arquivos = tb.Button(frame, text="Selecionar Arquivos", width=22, bootstyle=PRIMARY,
                                 command=self.selecionar_arquivos)
        btn_arquivos.pack(pady=(0, 10))
        # Títulos das colunas
        col_frame = tb.Frame(frame)
        col_frame.pack(fill=tb.X, pady=(0, 0))
        lbl_arquivo = tb.Label(col_frame, text="Arquivo", font=(
            "Segoe UI", 10, "bold"), anchor="center")
        lbl_arquivo.grid(row=0, column=0, sticky="ew",
                         padx=(0, 5), pady=(0, 2))
        lbl_trat = tb.Label(col_frame, text="ID Tratamento", font=(
            "Segoe UI", 10, "bold"), anchor="center")
        lbl_trat.grid(row=0, column=1, sticky="ew", padx=(0, 5), pady=(0, 2))
        col_frame.grid_columnconfigure(0, weight=2)
        col_frame.grid_columnconfigure(1, weight=1)
        # Tabela de arquivos
        tabela_frame = tb.Frame(frame, bootstyle="secondary")
        tabela_frame.pack(fill=tb.BOTH, expand=True, pady=(0, 10), padx=0)
        self.tabela_frame = tabela_frame
        self.frame_arquivos = tb.Frame(tabela_frame, bootstyle="secondary")
        self.frame_arquivos.pack(fill=tb.BOTH, expand=True, padx=1, pady=1)
        # Botões embaixo
        btns_frame = tb.Frame(frame)
        btns_frame.pack(pady=(10, 0), fill=tb.X)
        btn_processar = tb.Button(btns_frame, text="Processar", width=18, bootstyle=SUCCESS,
                                  command=self.processar)
        btn_processar.pack(side='left', padx=(0, 12), expand=True)
        btn_saida = tb.Button(btns_frame, text="Abrir pasta de saída", width=20, bootstyle=SECONDARY,
                              command=self.abrir_pasta_saida)
        btn_saida.pack(side='left', expand=True)

    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione um ou mais arquivos CSV de entrada",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        if arquivos:
            self.arquivos = list(arquivos)
            self.atualizar_campos_arquivos()

    def atualizar_campos_arquivos(self):
        for widget in self.frame_arquivos.winfo_children():
            widget.destroy()
        self.entries = []
        self.labels = []
        for idx, arquivo in enumerate(self.arquivos):
            row_frame = tb.Frame(self.frame_arquivos)
            row_frame.pack(fill=tb.X, pady=0, padx=0)
            nome = os.path.basename(arquivo)
            lbl = tb.Label(row_frame, text=nome, anchor="w", font=("Segoe UI", 10), cursor="hand2",
                           foreground="#2563eb", bootstyle="secondary")
            lbl.pack(side='left', fill=tb.X, expand=True, padx=(0, 5), pady=2)
            lbl.bind("<Button-1>", lambda e,
                     arq=arquivo: abrir_arquivo_csv(arq))
            entry = tb.Entry(row_frame, width=18, font=("Segoe UI", 10))
            entry.insert(0, "trat")
            entry.pack(side='left', padx=(0, 5), pady=2)
            # Botão X para remover arquivo
            btn_remover = tb.Button(row_frame, text="✕", width=2, bootstyle=DANGER,
                                    command=lambda i=idx: self.remover_arquivo(i))
            btn_remover.pack(side='left', padx=(5, 0), pady=2)
            self.labels.append(lbl)
            self.entries.append(entry)
            # Linha separadora
            sep = tb.Separator(self.frame_arquivos, orient="horizontal")
            sep.pack(fill=tb.X, pady=(0, 0))
        self.frame_arquivos.update_idletasks()
        self.geometry("")
        self._center_window()

    def remover_arquivo(self, idx):
        if 0 <= idx < len(self.arquivos):
            del self.arquivos[idx]
            self.atualizar_campos_arquivos()

    def processar(self):
        if not self.arquivos or not self.entries:
            messagebox.showerror(
                "Erro", "Selecione os arquivos e informe as chaves de tratamento.")
            return
        pasta_base = os.path.dirname(os.path.abspath(__file__))
        pasta_saida = os.path.join(pasta_base, "saida")
        os.makedirs(pasta_saida, exist_ok=True)
        resultados = []
        for arquivo, entry in zip(self.arquivos, self.entries):
            chave = entry.get().strip()
            if not chave:
                chave = "trat"
            nome = os.path.splitext(os.path.basename(arquivo))[0]
            ext = os.path.splitext(arquivo)[1]
            saida = os.path.join(pasta_saida, f"{nome}_extraido{ext}")
            linhas = extrair_dados_irga_csv(arquivo, saida, chave)
            resultados.append(
                f"{os.path.basename(saida)}: {linhas} linhas extraídas")
        messagebox.showinfo("Processamento concluído", "\n".join(resultados))
        abrir_saida(pasta_saida)

    def abrir_pasta_saida(self):
        pasta_base = os.path.dirname(os.path.abspath(__file__))
        pasta_saida = os.path.join(pasta_base, "saida")
        abrir_saida(pasta_saida)


if __name__ == "__main__":
    app = ExtratorApp()
    app.mainloop()
