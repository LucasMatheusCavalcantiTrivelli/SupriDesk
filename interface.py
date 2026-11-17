import tkinter as tk
from tkinter import messagebox, ttk

import regras
from database import Database


class SupriDeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SupriDesk")
        self.centralizar_janela(self.root, 800, 500)
        
        self.db = Database()
        
        self.criar_filtros_e_acoes()
        self.criar_tabela()
        self.atualizar_tabela()

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_sistema)

    def centralizar_janela(self, janela, largura, altura):
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)

        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def abrir_janela_cadastro(self):
        self.janela_cad = tk.Toplevel(self.root)
        self.janela_cad.title("Cadastrar Nova Solicitação")
        self.centralizar_janela(self.janela_cad, 400, 250)
        self.janela_cad.transient(self.root)
        self.janela_cad.grab_set()

        tk.Label(self.janela_cad, text="Setor:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_setor = tk.Entry(self.janela_cad, width=25)
        self.entry_setor.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.janela_cad, text="Material:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_material = tk.Entry(self.janela_cad, width=25)
        self.entry_material.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.janela_cad, text="Quantidade:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantidade = tk.Entry(self.janela_cad, width=25)
        self.entry_quantidade.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.janela_cad, text="Prioridade:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.combo_prioridade = ttk.Combobox(self.janela_cad, values=["Normal", "Alta"], state="readonly", width=23)
        self.combo_prioridade.set("Normal")
        self.combo_prioridade.grid(row=3, column=1, padx=10, pady=10)

        btn_salvar = tk.Button(self.janela_cad, text="Salvar Solicitação", command=self.cadastrar, bg="green", fg="white")
        btn_salvar.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew", padx=10)

    def criar_filtros_e_acoes(self):
        self.filtro_frame = tk.Frame(self.root, padx=10, pady=10)
        self.filtro_frame.pack(fill="x", side="top")

        tk.Label(self.filtro_frame, text="Buscar (Setor/Material):").pack(side="left")
        self.entry_busca = tk.Entry(self.filtro_frame)
        self.entry_busca.pack(side="left", padx=5)

        tk.Label(self.filtro_frame, text="Status:").pack(side="left", padx=(10, 0))
        self.combo_filtro_status = ttk.Combobox(self.filtro_frame, values=["Todos", "Pendente", "Em atendimento", "Atendida"], state="readonly", width=15)
        self.combo_filtro_status.set("Todos")
        self.combo_filtro_status.pack(side="left", padx=5)

        self.btn_buscar = tk.Button(self.filtro_frame, text="Buscar", command=self.atualizar_tabela)
        self.btn_buscar.pack(side="left", padx=5)

        self.btn_limpar = tk.Button(self.filtro_frame, text="Limpar Filtros", command=self.limpar_filtros)
        self.btn_limpar.pack(side="left", padx=5)

    def criar_tabela(self):
        self.tabela_frame = tk.Frame(self.root, padx=10, pady=10)
        self.tabela_frame.pack(fill="both", expand=True)

        colunas = ("id", "setor", "material", "quantidade", "prioridade", "status", "data_hora")
        self.tree = ttk.Treeview(self.tabela_frame, columns=colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40, anchor="center")

        self.tree.heading("setor", text="Setor")
        self.tree.column("setor", width=100, anchor="center")
        
        self.tree.heading("material", text="Material")
        self.tree.column("material", width=150, anchor="center")
        
        self.tree.heading("quantidade", text="Qtd")
        self.tree.column("quantidade", width=50, anchor="center")
        
        self.tree.heading("prioridade", text="Prioridade")
        self.tree.column("prioridade", width=80, anchor="center")
        
        self.tree.heading("status", text="Status")
        self.tree.column("status", width=100, anchor="center")
        
        self.tree.heading("data_hora", text="Data/Hora")
        self.tree.column("data_hora", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.acoes_frame = tk.Frame(self.root, pady=10, padx=10)
        self.acoes_frame.pack(fill="x")

        self.btn_abrir_cadastro = tk.Button(
            self.acoes_frame, 
            text="➕ Nova Solicitação", 
            command=self.abrir_janela_cadastro, 
            bg="green", 
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_abrir_cadastro.pack(side="left", padx=(0, 10))
        
        self.btn_avancar = tk.Button(self.acoes_frame, text="Avançar Status", command=self.avancar_status, bg="blue", fg="white")
        self.btn_avancar.pack(side="left", padx=10)
        
        self.btn_exportar = tk.Button(self.acoes_frame, text="Exportar CSV", command=self.exportar_csv, bg="orange", fg="white")
        self.btn_exportar.pack(side="left", padx=10)

        self.btn_excluir = tk.Button(self.acoes_frame, text="Excluir", command=self.excluir_solicitacao, bg="red", fg="white")
        self.btn_excluir.pack(side="right", padx=10)

    def cadastrar(self):
        setor = self.entry_setor.get()
        material = self.entry_material.get()
        quantidade = self.entry_quantidade.get()
        prioridade = self.combo_prioridade.get()

        valido, mensagem = regras.validar_cadastro(setor, material, quantidade, prioridade)
        
        if not valido:
            messagebox.showerror("Erro de Validação", mensagem)
            return
        
        data_hora = regras.obter_data_hora_atual()
        self.db.inserir_solicitacao(setor, material, int(quantidade), prioridade, data_hora)

        self.entry_setor.delete(0, tk.END)
        self.entry_material.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.combo_prioridade.set("Normal")

        self.atualizar_tabela()
        messagebox.showinfo("Sucesso", "Solicitação cadastrada com sucesso!")

        self.janela_cad.destroy()

    def avancar_status(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma solicitação na tabela primeiro.")
            return
        
        valores = self.tree.item(selecionado[0], "values")
        id_solicitacao = valores[0]
        status_atual = valores[5]

        proximo_status = regras.obter_proximo_status(status_atual)

        if proximo_status is None:
            messagebox.showerror("Bloqueado", f"A solicitação já está '{status_atual}' e não pode avançar.")
            return
        
        self.db.atualizar_status(id_solicitacao, proximo_status)
        self.atualizar_tabela()
        messagebox.showinfo("Sucesso", f"Status alterado para: {proximo_status}")

    def excluir_solicitacao(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma solicitação na tabela para excluir.")
            return
        
        valores = self.tree.item(selecionado[0], "values")
        id_solicitacao = valores[0]
        material = valores[2]

        confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a solicitação do material '{material}'?")
        
        if confirmacao:
            self.db.deletar_solicitacao(id_solicitacao)
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Solicitação excluída com sucesso.")

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termo = self.entry_busca.get() if hasattr(self, 'entry_busca') else ""
        status = self.combo_filtro_status.get() if hasattr(self, 'combo_filtro_status') else "Todos"
        
        registros = self.db.listar_solicitacoes(termo, status)
        
        for linha in registros:
            self.tree.insert("", "end", values=linha)

    def limpar_filtros(self):
        self.entry_busca.delete(0, tk.END)
        self.combo_filtro_status.set("Todos")
        self.atualizar_tabela()

    def exportar_csv(self):
        import csv
        registros = self.db.listar_solicitacoes()
        
        if not registros:
            messagebox.showwarning("Aviso", "Não há dados para exportar.")
            return
          
        try:
            with open("historico_solicitacoes.csv", "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo, delimiter=";")
                escritor.writerow(["ID", "Setor", "Material", "Quantidade", "Prioridade", "Status", "Data/Hora"])
                escritor.writerows(registros)
                
            messagebox.showinfo("Sucesso", "Histórico exportado para 'historico_solicitacoes.csv'!")
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

    def fechar_sistema(self):
        self.db.fechar()
        self.root.destroy()