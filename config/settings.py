# Centraliza as configurações. Se futuramente quisermos usar um .env para carregar o caminho do bin do PostgreSQL, será feito apenas aqui.

import os

# Caminhos do PostgreSQL
PG_BIN_DIR = os.getenv("PG_BIN_DIR", r"C:\pgsql\bin")
PG_DUMP = os.path.join(PG_BIN_DIR, "pg_dump.exe")
PG_RESTORE = os.path.join(PG_BIN_DIR, "pg_restore.exe")

# URLs Padrão de Exemplo
DEFAULT_BACKUP_URL = "postgresql://user:pass@host:5432/dbname?sslmode=require"
DEFAULT_RESTORE_URL = (
    "postgresql://postgres:senha_local@localhost:5432/laboratorios_teste"
)
