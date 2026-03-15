import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from webscraper import ehValido, getInfo


# ===== Cores e Estilo =====

COLORS = {
    "bg": "#0f0f1a",
    "bg_secondary": "#1a1a2e",
    "bg_entry": "#16162b",
    "fg": "#e8e8f0",
    "fg_secondary": "#8888aa",
    "accent": "#7c5ce7",
    "accent_hover": "#9b7dff",
    "accent_dark": "#5a3db5",
    "success": "#10b981",
    "error": "#ef4444",
    "border": "#2a2a45",
    "highlight": "#222240",
}


# ===== Aplicação =====

class WebScraperApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("WebScraper — Wikipedia PT")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(750, 600)
        self.root.geometry("850x700")

        # Estilo ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        self._build_ui()

    def _configure_styles(self):
        s = self.style

        s.configure("TFrame", background=COLORS["bg"])
        s.configure("Secondary.TFrame", background=COLORS["bg_secondary"])

        s.configure("Title.TLabel",
                     background=COLORS["bg"],
                     foreground=COLORS["accent"],
                     font=("Segoe UI", 22, "bold"))

        s.configure("Subtitle.TLabel",
                     background=COLORS["bg"],
                     foreground=COLORS["fg_secondary"],
                     font=("Segoe UI", 10))

        s.configure("TLabel",
                     background=COLORS["bg"],
                     foreground=COLORS["fg"],
                     font=("Segoe UI", 10))

        s.configure("Status.TLabel",
                     background=COLORS["bg"],
                     foreground=COLORS["fg_secondary"],
                     font=("Segoe UI", 9))

        s.configure("Article.TLabel",
                     background=COLORS["bg"],
                     foreground=COLORS["success"],
                     font=("Segoe UI", 11, "bold"))

        s.configure("Error.TLabel",
                     background=COLORS["bg"],
                     foreground=COLORS["error"],
                     font=("Segoe UI", 10))

        # Notebook (abas)
        s.configure("TNotebook",
                     background=COLORS["bg"],
                     borderwidth=0)
        s.configure("TNotebook.Tab",
                     background=COLORS["bg_secondary"],
                     foreground=COLORS["fg_secondary"],
                     font=("Segoe UI", 9),
                     padding=[12, 5])
        s.map("TNotebook.Tab",
              background=[("selected", COLORS["accent_dark"])],
              foreground=[("selected", COLORS["fg"])],
              font=[("selected", ("Segoe UI", 11, "bold"))],
              padding=[("selected", [20, 10])])

        # Treeview (listas)
        s.configure("Custom.Treeview",
                     background=COLORS["bg_secondary"],
                     foreground=COLORS["fg"],
                     fieldbackground=COLORS["bg_secondary"],
                     borderwidth=0,
                     font=("Segoe UI", 9),
                     rowheight=28)
        s.map("Custom.Treeview",
              background=[("selected", COLORS["accent_dark"])],
              foreground=[("selected", "#ffffff")])
        s.configure("Custom.Treeview.Heading",
                     background=COLORS["border"],
                     foreground=COLORS["fg_secondary"],
                     font=("Segoe UI", 9, "bold"),
                     borderwidth=0)
        s.map("Custom.Treeview.Heading",
              background=[("active", COLORS["highlight"])])

    def _build_ui(self):
        # Container principal
        main = ttk.Frame(self.root, style="TFrame")
        main.pack(fill="both", expand=True, padx=24, pady=20)

        # Cabeçalho
        ttk.Label(main, text="🕷️  WebScraper", style="Title.TLabel").pack(anchor="w")
        ttk.Label(main, text="Extraia informações de artigos da Wikipedia PT",
                  style="Subtitle.TLabel").pack(anchor="w", pady=(0, 16))

        # Barra de busca
        search_frame = ttk.Frame(main, style="TFrame")
        search_frame.pack(fill="x", pady=(0, 12))

        self.url_var = tk.StringVar()
        self.entry = tk.Entry(
            search_frame,
            textvariable=self.url_var,
            font=("Segoe UI", 11),
            bg=COLORS["bg_entry"],
            fg=COLORS["fg"],
            insertbackground=COLORS["accent"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self._on_search())

        self.search_btn = tk.Button(
            search_frame,
            text="🔍  Buscar",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["accent"],
            fg="#ffffff",
            activebackground=COLORS["accent_hover"],
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            command=self._on_search,
        )
        self.search_btn.pack(side="right")

        # Status
        self.status_var = tk.StringVar(value="Cole uma URL e clique em Buscar")
        self.status_label = ttk.Label(main, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor="w", pady=(0, 4))

        # Nome do artigo
        self.article_var = tk.StringVar()
        self.article_label = ttk.Label(main, textvariable=self.article_var, style="Article.TLabel")
        self.article_label.pack(anchor="w", pady=(0, 8))

        # Abas de resultados
        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True)

        # Aba: Sumário
        toc_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(toc_frame, text="  📑 Sumário  ")
        self.toc_tree = self._create_treeview(toc_frame, columns=("#", "Título"),
                                               widths=(50, 600))

        # Aba: Imagens
        img_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(img_frame, text="  🖼️ Imagens  ")
        self.img_tree = self._create_treeview(img_frame, columns=("#", "Arquivo"),
                                               widths=(50, 600))

        # Aba: Links
        link_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(link_frame, text="  🔗 Links  ")
        self.link_tree = self._create_treeview(link_frame, columns=("#", "Artigo"),
                                                widths=(50, 600))

    def _create_treeview(self, parent, columns, widths):
        container = ttk.Frame(parent, style="TFrame")
        container.pack(fill="both", expand=True, pady=(8, 0))

        tree = ttk.Treeview(container, columns=columns, show="headings",
                            style="Custom.Treeview", selectmode="browse")

        for col, w in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, minwidth=40,
                       anchor="center" if col == "#" else "w")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return tree

    def _on_search(self):
        url = self.url_var.get().strip()
        url = re.sub(r'\s+', '', url)

        if not url:
            messagebox.showwarning("Atenção", "Digite uma URL.")
            return

        if not ehValido(url):
            messagebox.showerror("URL Inválida",
                                 "Use uma URL da Wikipedia PT.\nExemplo: https://pt.wikipedia.org/wiki/Python")
            return

        # Desabilita o botão e mostra loading
        self.search_btn.config(state="disabled", text="⏳ Buscando…")
        self.status_var.set("⏳ Extraindo dados do artigo…")
        self.style.configure("Status.TLabel", foreground=COLORS["accent"])
        self.article_var.set("")

        # Limpar listas
        for tree in (self.toc_tree, self.img_tree, self.link_tree):
            tree.delete(*tree.get_children())

        # Rodar em thread separada para não travar a interface
        thread = threading.Thread(target=self._do_scrape, args=(url,), daemon=True)
        thread.start()

    def _do_scrape(self, url: str):
        try:
            info = getInfo(url)
            self.root.after(0, self._show_results, info)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))

    def _show_results(self, info: dict):
        article = info["article"]
        toc = info["toc"]
        images = info["images"]
        links = info["links"]

        self.article_var.set(f"📄 {article}")
        self.status_var.set(
            f"✅ {len(toc)} itens no sumário  •  {len(images)} imagens  •  {len(links)} links"
        )
        self.style.configure("Status.TLabel", foreground=COLORS["success"])

        # Preencher Treeviews
        for i, item in enumerate(toc, 1):
            self.toc_tree.insert("", "end", values=(i, item))

        for i, item in enumerate(images, 1):
            self.img_tree.insert("", "end", values=(i, item))

        for i, item in enumerate(links, 1):
            self.link_tree.insert("", "end", values=(i, f"pt.wikipedia.org/wiki/{item}"))

        # Atualizar texto das abas com contadores
        self.notebook.tab(0, text=f"  📑 Sumário ({len(toc)})  ")
        self.notebook.tab(1, text=f"  🖼️ Imagens ({len(images)})  ")
        self.notebook.tab(2, text=f"  🔗 Links ({len(links)})  ")

        self.search_btn.config(state="normal", text="🔍  Buscar")

    def _show_error(self, msg: str):
        self.status_var.set(f"❌ {msg}")
        self.style.configure("Status.TLabel", foreground=COLORS["error"])
        self.search_btn.config(state="normal", text="🔍  Buscar")


# ===== Main =====

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
