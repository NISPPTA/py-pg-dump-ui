# 🛡️ PostgreSQL Backup & Restore GUI

Uma interface gráfica leve e responsiva construída em Python (Tkinter) para facilitar a execução de comandos `pg_dump` e `pg_restore`. Ideal para migrar bancos de dados de produção para ambientes de teste locais sem a necessidade de digitar comandos complexos no terminal.

## ✨ Funcionalidades

- **Execução Assíncrona:** Utiliza *threads* para garantir que a interface não congele durante dumps pesados.
- **Feedback em Tempo Real:** Terminal embutido exibindo logs das transações e barra de progresso animada.
- **Segurança Transacional:** Injeta automaticamente a flag `-1` na restauração (single transaction) para evitar bancos corrompidos em caso de erro.
- **Nativo e Leve:** Usa apenas bibliotecas padrão do Python (`tkinter`, `subprocess`, `threading`). Nenhuma dependência externa pesada.

## 🚀 Como usar

### Pré-requisitos
- Python 3.10+ instalado.
- Ferramentas de linha de comando do PostgreSQL (`pg_dump` e `pg_restore`) instaladas na sua máquina (por padrão em `C:\pgsql\bin` no Windows).

### Execução
1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_PROJETO.git](https://github.com/SEU_USUARIO/NOME_DO_PROJETO.git)
