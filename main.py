import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from functions import extrair_dados_irga
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
        self.colunas_padrao = ["Tratamento", "Obs", "HHMMSS"]
        self.colunas_possiveis = [
            "FTime", "EBal?", "Photo", "Cond", "Ci", "Trmmol", "VpdL", "CTleaf", "Area", "BLC_1", "StmRat", "BLCond", "Tair", "Tleaf", "TBlk", "CO2R", "CO2S", "H2OR", "H2OS", "RH_R", "RH_S", "Flow", "PARi", "PARo", "Press", "CsMch", "HsMch", "StableF", "BLCslope", "BLCoffst", "f_parin", "f_parout", "alphaK", "Status", "fda", "Trans", "Tair_K", "Twall_K", "R(W/m2)", "Tl-Ta", "SVTleaf", "h2o_i", "h20diff", "CTair", "SVTair", "CndTotal", "vp_kPa", "VpdA", "CndCO2", "Ci_Pa", "Ci/Ca", "RHsfc", "C2sfc", "AHs/Cs"
        ]
        self.check_vars = []
        # Botão de selecionar arquivos no topo
        btn_arquivos = tb.Button(frame, text="Selecionar Arquivos", width=22, bootstyle=PRIMARY,
                                 command=self.selecionar_arquivos)
        btn_arquivos.pack(pady=(0, 10))
        # Espaço para seleção de variáveis
        self.lbl_vars = tb.Label(
            frame, text="Selecione as variáveis a exportar:", font=("Segoe UI", 10, "bold"))
        self.vars_frame = tb.Frame(frame)
        # Não exibe inicialmente
        self.lbl_vars.pack_forget()
        self.vars_frame.pack_forget()
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
        tabela_frame = tb.Frame(frame)  # Removido bootstyle="secondary"
        tabela_frame.pack(fill=tb.BOTH, expand=True, pady=(0, 10), padx=0)
        self.tabela_frame = tabela_frame
        # Removido bootstyle="secondary"
        self.frame_arquivos = tb.Frame(tabela_frame)
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
            filetypes=[
                ("Arquivos CSV", "*.csv")
            ]
        )
        if arquivos:
            self.arquivos = list(arquivos)
            self._atualizar_checkboxes_colunas()
            self.atualizar_campos_arquivos()

    def _atualizar_checkboxes_colunas(self):
        self.lbl_vars.pack(anchor="w", pady=(0, 2))
        self.vars_frame.pack(fill=tb.X, pady=(0, 10))
        for widget in self.vars_frame.winfo_children():
            widget.destroy()
        colunas_encontradas = []
        tipos_colunas = []
        for arquivo in self.arquivos:
            try:
                with open(arquivo, encoding='utf-8') as f:
                    import csv
                    reader = csv.reader(f)
                    header = None
                    tipo = None
                    for row in reader:
                        if row and row[0].strip().lower().startswith('obs'):
                            header = row
                        elif header and not tipo and any(cell.strip().lower() in ['in', 'out'] for cell in row):
                            tipo = row
                            break
                    if header:
                        colunas_encontradas = header
                        if tipo:
                            tipos_colunas = tipo
                        break
            except Exception:
                continue
        colunas_padrao = ["Tratamento", "Obs", "HHMMSS"]
        colunas_opcionais = [
            c for c in colunas_encontradas if c not in colunas_padrao]
        # Organiza por tipo (in/out)
        in_vars = [c for c, t in zip(colunas_encontradas, tipos_colunas) if t.strip(
        ).lower() == 'in' and c not in colunas_padrao]
        out_vars = [c for c, t in zip(colunas_encontradas, tipos_colunas) if t.strip(
        ).lower() == 'out' and c not in colunas_padrao]
        self.colunas_padrao = colunas_padrao
        self.colunas_possiveis = in_vars + out_vars
        self.check_vars = []
        # Cria frames separados para in/out (layout vertical)
        in_frame = tb.LabelFrame(self.vars_frame, text='Variáveis IN')
        in_frame.pack(fill=tb.X, expand=True, padx=8, pady=(0, 4))
        out_frame = tb.LabelFrame(self.vars_frame, text='Variáveis OUT')
        out_frame.pack(fill=tb.X, expand=True, padx=8, pady=(0, 4))
        for i, var in enumerate(in_vars):
            var_chk = tk.IntVar(value=-1)
            chk = tb.Checkbutton(in_frame, text=var,
                                 variable=var_chk, bootstyle=INFO)
            chk.state(['alternate'])
            chk.grid(row=i//8, column=i % 8, sticky="w", padx=2, pady=1)
            self.check_vars.append((var, var_chk))
        for i, var in enumerate(out_vars):
            var_chk = tk.IntVar(value=-1)
            chk = tb.Checkbutton(out_frame, text=var,
                                 variable=var_chk, bootstyle=INFO)
            chk.state(['alternate'])
            chk.grid(row=i//8, column=i % 8, sticky="w", padx=2, pady=1)
            self.check_vars.append((var, var_chk))

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
            entry = tb.Entry(row_frame, width=28, font=("Segoe UI", 10))
            entry.insert(0, "trat")
            entry.pack(side='left', padx=(0, 5), pady=2)
            # Balão de dica para múltiplas chaves
            self._add_tooltip(
                entry, "Separe múltiplos tratamentos por vírgula, ex: trat1, trat2")
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

    def _add_tooltip(self, widget, text):
        # Balão de dica simples para widgets Tkinter/ttkbootstrap
        def on_enter(event):
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief='solid', borderwidth=1,
                             font=("Segoe UI", 9), padx=6, pady=2)
            label.pack()
            # Fecha o balão após 3 segundos
            self.tooltip.after(3000, lambda: self._close_tooltip())

        def on_leave(event):
            self._close_tooltip()
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def _close_tooltip(self):
        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

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
        # Coleta variáveis selecionadas
        colunas_selecionadas = [var for var,
                                var_chk in self.check_vars if var_chk.get()]
        if colunas_selecionadas:
            colunas_exportar = self.colunas_padrao + colunas_selecionadas
        else:
            colunas_exportar = None  # Exporta todas se nada selecionado
        for arquivo, entry in zip(self.arquivos, self.entries):
            chave = entry.get().strip()
            if not chave:
                chave = "trat"
            # Permite múltiplas chaves separadas por vírgula
            if ',' in chave:
                chaves = [c.strip() for c in chave.split(',') if c.strip()]
            else:
                chaves = chave
            nome = os.path.splitext(os.path.basename(arquivo))[0]
            ext = os.path.splitext(arquivo)[1]
            saida = os.path.join(pasta_saida, f"{nome}_extraido{ext}")
            linhas = extrair_dados_irga(
                arquivo, saida, chaves, colunas_exportar)
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
