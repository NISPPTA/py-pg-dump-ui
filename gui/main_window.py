# A interface gráfica. Ela mapeia os callbacks do Core de volta para a 
# thread principal do Tkinter usando self.root.after, garantindo que a tela não congele.

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from config import settings
from core.postgres_runner import PostgresRunner


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PostgreSQL Vault - Backup & Restore UI")
        self.root.geometry("750x740")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")

        # Instancia o Core (Runner), passando os métodos seguros para Thread
        self.runner = PostgresRunner(
            on_log=self.safe_log_message,
            on_state_change=self.safe_toggle_ui,
        )

        self._create_widgets()

    def _create_widgets(self):
        # --- SEÇÃO DE VERSÃO DO MOTOR ---
        engine_frame = ttk.LabelFrame(
            self.root, text=" Motor Cliente PostgreSQL ", padding=(10, 8)
        )
        engine_frame.pack(fill="x", padx=15, pady=(10, 5))

        ttk.Label(engine_frame, text="Versão dos Binários:").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.combo_version = ttk.Combobox(
            engine_frame,
            values=list(settings.PG_VERSIONS.keys()),
            state="readonly",
            width=45,
        )
        self.combo_version.set(settings.DEFAULT_PG_VERSION)
        self.combo_version.grid(row=0, column=1, sticky="w", padx=5)

        # --- SEÇÃO DE BACKUP ---
        backup_frame = ttk.LabelFrame(
            self.root, text=" 1. Backup (Produção -> Arquivo Local) ", padding=(10, 10)
        )
        backup_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(backup_frame, text="URL Origem:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_backup_url = ttk.Entry(backup_frame, width=70)
        self.entry_backup_url.grid(row=0, column=1, columnspan=2, pady=5, padx=5)
        self.entry_backup_url.insert(0, settings.DEFAULT_BACKUP_URL)

        ttk.Label(backup_frame, text="Salvar em:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_backup_path = ttk.Entry(backup_frame, width=55)
        self.entry_backup_path.grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(
            backup_frame, text="Procurar...", command=self.browse_backup_save
        ).grid(row=1, column=2, pady=5)

        self.btn_run_backup = ttk.Button(
            backup_frame, text="▶ INICIAR BACKUP", command=self.action_backup
        )
        self.btn_run_backup.grid(row=2, column=0, columnspan=3, pady=10)

        # --- SEÇÃO DE RESTAURAÇÃO ---
        restore_frame = ttk.LabelFrame(
            self.root,
            text=" 2. Restauração (Arquivo Local -> Banco Teste) ",
            padding=(10, 10),
        )
        restore_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(restore_frame, text="Arquivo:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_restore_path = ttk.Entry(restore_frame, width=55)
        self.entry_restore_path.grid(row=0, column=1, pady=5, padx=5)

        ttk.Button(
            restore_frame, text="Procurar...", command=self.browse_restore_open
        ).grid(row=0, column=2, pady=5)

        ttk.Label(restore_frame, text="URL Destino:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_restore_url = ttk.Entry(restore_frame, width=70)
        self.entry_restore_url.grid(row=1, column=1, columnspan=2, pady=5, padx=5)
        self.entry_restore_url.insert(0, settings.DEFAULT_RESTORE_URL)

        self.btn_run_restore = ttk.Button(
            restore_frame, text="▶ INICIAR RESTAURAÇÃO", command=self.action_restore
        )
        self.btn_run_restore.grid(row=2, column=0, columnspan=3, pady=10)

        # --- PROGRESSO E TERMINAL ---
        self.progress_bar = ttk.Progressbar(
            self.root, mode="indeterminate", orient="horizontal"
        )
        self.progress_bar.pack(fill="x", padx=15, pady=5)

        log_frame = ttk.LabelFrame(
            self.root, text=" Terminal de Saída ", padding=(10, 10)
        )
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.log_area = ScrolledText(
            log_frame,
            wrap=tk.WORD,
            height=10,
            bg="black",
            fg="lightgreen",
            font=("Consolas", 9),
        )
        self.log_area.pack(fill="both", expand=True)
        self.log_area.insert(tk.END, "Aguardando comandos (Sistema isolado)...\n")
        self.log_area.configure(state="disabled")

    # --- FUNÇÕES DE SELEÇÃO DE ARQUIVO ---
    def browse_backup_save(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".dump", filetypes=[("PG Dump", "*.dump"), ("All", "*.*")]
        )
        if filename:
            self.entry_backup_path.delete(0, tk.END)
            self.entry_backup_path.insert(0, filename)

    def browse_restore_open(self):
        filename = filedialog.askopenfilename(
            filetypes=[("PG Dump", "*.dump"), ("All", "*.*")]
        )
        if filename:
            self.entry_restore_path.delete(0, tk.END)
            self.entry_restore_path.insert(0, filename)

    # --- THREAD-SAFE CALLBACKS PARA UI ---
    def safe_log_message(self, message):
        self.root.after(0, self._ui_log, message)

    def safe_toggle_ui(self, is_idle):
        self.root.after(0, self._ui_toggle, is_idle)

    def _ui_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def _ui_toggle(self, is_idle):
        status = tk.NORMAL if is_idle else tk.DISABLED
        self.btn_run_backup.configure(state=status)
        self.btn_run_restore.configure(state=status)
        self.combo_version.configure(state="readonly" if is_idle else tk.DISABLED)
        self.progress_bar.stop() if is_idle else self.progress_bar.start(15)

    # --- AÇÕES DOS BOTÕES ---
    def _get_selected_bin_dir(self):
        selected_label = self.combo_version.get()
        return settings.PG_VERSIONS[selected_label]

    def action_backup(self):
        url = self.entry_backup_url.get().strip()
        path = self.entry_backup_path.get().strip()
        if not url or not path:
            messagebox.showwarning(
                "Aviso", "Preencha a URL de origem e o destino do arquivo."
            )
            return
        self.runner.run_backup(url, path, self._get_selected_bin_dir())

    def action_restore(self):
        url = self.entry_restore_url.get().strip()
        path = self.entry_restore_path.get().strip()
        if not url or not path:
            messagebox.showwarning(
                "Aviso", "Preencha a URL de destino e o arquivo fonte."
            )
            return
        self.runner.run_restore(url, path, self._get_selected_bin_dir())
