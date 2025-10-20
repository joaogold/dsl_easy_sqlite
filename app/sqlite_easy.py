import sqlite3
import os

db_structure = {
    "banco": "meu_banco.db",
    "tabelas": {
        "usuarios": {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "nome": "TEXT NOT NULL",
            "email": "TEXT UNIQUE NOT NULL",
            "idade": "INTEGER"
        },
        "produtos": {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "nome": "TEXT NOT NULL",
            "preco": "REAL NOT NULL",
            "quantidade": "INTEGER DEFAULT 0"
        }
    }
}

def criar_banco_e_tabelas(structure: dict):
    resultado = {
        "banco_existe": False,
        "tabelas_criadas": [],
        "tabelas_existentes": []
    }

    banco = structure["banco"]
    tabelas = structure["tabelas"]

    # Verifica se o banco existe
    if os.path.exists(banco):
        resultado["banco_existe"] = True

    # Conecta ou cria o banco
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()

    # Loop para criar tabelas
    for tabela, colunas in tabelas.items():
        # Monta comando SQL para criar tabela
        colunas_sql = ", ".join([f"{nome} {tipo}" for nome, tipo in colunas.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {tabela} ({colunas_sql})"
        cursor.execute(sql)
        
        # Verifica se tabela já existia
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabela,))
        if cursor.fetchone():
            resultado["tabelas_existentes"].append(tabela)
        else:
            resultado["tabelas_criadas"].append(tabela)

    conn.commit()
    conn.close()
    return resultado