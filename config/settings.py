import os
from pathlib import Path

# Descobre a pasta raiz do projeto dinamicamente (sobe um nível a partir de /config)
BASE_DIR = Path(__file__).resolve().parent.parent

# Aponta para a pasta pgsql/bin embutida dentro do projeto
PG_BIN_DIR = os.getenv("PG_BIN_DIR", str(BASE_DIR / "pgsql" / "bin"))

PG_DUMP = os.path.join(PG_BIN_DIR, "pg_dump.exe")
PG_RESTORE = os.path.join(PG_BIN_DIR, "pg_restore.exe")

# URLs Padrão de Exemplo
DEFAULT_BACKUP_URL = "postgresql://user:pass@host:5432/dbname?sslmode=require"
DEFAULT_RESTORE_URL = "postgresql://postgres:senha_local@localhost:5432/laboratorios_teste"