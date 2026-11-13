from pathlib import Path

# Descobre a pasta raiz do projeto dinamicamente (sobe um nível a partir de /config)
BASE_DIR = Path(__file__).resolve().parent.parent
PG_BASE_DIR = BASE_DIR / "pgsql"

# Mapeamento das versões portáteis embutidas no projeto
PG_VERSIONS = {
    "PostgreSQL 18.7 (Nuvem / Neon)": PG_BASE_DIR / "v18" / "bin",
    "PostgreSQL 17.10 (Servidor Local)": PG_BASE_DIR / "v17" / "bin",
}

DEFAULT_PG_VERSION = "PostgreSQL 18.7 (Nuvem / Neon)"

# URLs Padrão de Exemplo
DEFAULT_BACKUP_URL = "postgresql://user:pass@host:5432/dbname?sslmode=require"
DEFAULT_RESTORE_URL = (
    "postgresql://postgres:senha_local@localhost:5432/laboratorios_teste"
)
