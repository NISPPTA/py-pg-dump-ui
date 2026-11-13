# O motor DBA. Completamente agnóstico de Tkinter. Ele apenas processa os dumps e usa callbacks para avisar o chamador (a GUI) sobre o que está acontecendo.

import os
import subprocess
import threading


class PostgresRunner:
    def __init__(self, pg_dump_path, pg_restore_path, on_log, on_state_change):
        """
        :param on_log: Função callback para enviar mensagens de log.
        :param on_state_change: Função callback para alterar estado UI (bloquear/liberar botões).
        """
        self.pg_dump = pg_dump_path
        self.pg_restore = pg_restore_path
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
                "\n❌ ERRO: Executável não encontrado. Verifique o caminho no config/settings.py."
            )
        except Exception as e:
            self.on_log(f"\n❌ ERRO FATAL: {e!s}")
        finally:
            self.on_state_change(True)
            self.on_log("=" * 50 + "\n")

    def run_backup(self, url, filepath):
        cmd = [self.pg_dump, url, "-v", "-F", "c", "-f", filepath]
        threading.Thread(
            target=self._execute_command,
            args=(cmd, "BACKUP CONCLUÍDO COM SUCESSO!"),
            daemon=True,
        ).start()

    def run_restore(self, url, filepath):
        cmd = [self.pg_restore, "-d", url, "-v", "-1", filepath]
        threading.Thread(
            target=self._execute_command,
            args=(cmd, "RESTAURAÇÃO CONCLUÍDA COM SUCESSO!"),
            daemon=True,
        ).start()
