# O motor DBA. Completamente agnóstico de Tkinter. Ele apenas processa os dumps e usa callbacks para avisar o chamador (a GUI) sobre o que está acontecendo.

import os
import subprocess
import threading
from pathlib import Path


class PostgresRunner:
    def __init__(self, on_log, on_state_change):
        """
        :param on_log: Função callback para enviar mensagens de log.
        :param on_state_change: Função callback para alterar estado UI (bloquear/liberar botões).
        """
        self.on_log = on_log
        self.on_state_change = on_state_change

    def _execute_command(self, cmd, success_msg):
        self.on_state_change(False)
        self.on_log(f"Executando: {' '.join(cmd)}\n{'-' * 50}")

        try:
            # subprocess.CREATE_NO_WINDOW (Valor 0x08000000) suprime o CMD no Windows
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
                creationflags=0x08000000 if os.name == "nt" else 0,
            )

            for line in process.stdout:
                self.on_log(line.strip())

            process.wait()

            if process.returncode == 0:
                self.on_log(f"\n✅ {success_msg}")
            else:
                self.on_log(f"\n❌ Operação falhou com código: {process.returncode}")

        except FileNotFoundError:
            self.on_log(
                "\n❌ ERRO: Executável não encontrado na pasta da versão selecionada."
            )
        except (OSError, subprocess.SubprocessError, ValueError) as e:
            self.on_log(f"\n❌ ERRO FATAL: {e!s}")
        finally:
            self.on_state_change(True)
            self.on_log("=" * 50 + "\n")

    def run_backup(self, url: str, filepath: str, bin_dir: Path):
        pg_dump = str(bin_dir / "pg_dump.exe")
        cmd = [pg_dump, url, "-v", "-F", "c", "-f", filepath]
        threading.Thread(
            target=self._execute_command,
            args=(cmd, "BACKUP CONCLUÍDO COM SUCESSO!"),
            daemon=True,
        ).start()

    def run_restore(self, url: str, filepath: str, bin_dir: Path):
        pg_restore = str(bin_dir / "pg_restore.exe")
        # --no-owner evita erros com a role neondb_owner no banco local
        # Sem -1 para o PG 17 não abortar no aviso de transaction_timeout do PG 18
        cmd = [pg_restore, "-d", url, "-v", "--no-owner", filepath]
        threading.Thread(
            target=self._execute_command,
            args=(cmd, "RESTAURAÇÃO CONCLUÍDA COM SUCESSO!"),
            daemon=True,
        ).start()
