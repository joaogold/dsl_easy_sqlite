import sqlite3
import os

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


def adicionar_dados(banco: str, tabela: str, dados: dict):
    """
    Adiciona dados em uma tabela do banco.
    
    :param banco: nome do banco .db
    :param tabela: nome da tabela
    :param dados: dicionário com colunas e valores
    :return: resultado em dicionário
    """
    resultado = {"sucesso": False, "mensagem": "", "dados_inseridos": dados}
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()

        colunas = ", ".join(dados.keys())
        valores_placeholder = ", ".join(["?" for _ in dados])
        valores = tuple(dados.values())

        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores_placeholder})"
        cursor.execute(sql)
        conn.commit()
        conn.close()

        resultado["sucesso"] = True
        resultado["mensagem"] = "Dados inseridos com sucesso"
    except Exception as e:
        resultado["mensagem"] = str(e)
    
    return resultado

def pesquisar_dados(banco: str, tabela: str, filtros: dict = None):
    """
    Pesquisa dados em uma tabela com filtros opcionais.
    
    :param banco: nome do banco
    :param tabela: nome da tabela
    :param filtros: dicionário {coluna: valor} para filtrar resultados
    :return: lista de resultados
    """
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()

    sql = f"SELECT * FROM {tabela}"
    valores = ()

    if filtros:
        condicoes = " AND ".join([f"{col} = ?" for col in filtros.keys()])
        sql += f" WHERE {condicoes}"
        valores = tuple(filtros.values())

    cursor.execute(sql, valores)
    colunas = [descricao[0] for descricao in cursor.description]
    resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    conn.close()
    return resultados

def excluir_dados(banco: str, tabela: str, filtros: dict):
    """
    Exclui dados de uma tabela com base em filtros.
    
    :param banco: nome do banco .db
    :param tabela: nome da tabela
    :param filtros: dicionário {coluna: valor} para definir quais registros excluir
    :return: dicionário com resultado da operação
    """
    resultado = {"sucesso": False, "mensagem": "", "filtros": filtros}
    
    if not filtros:
        resultado["mensagem"] = "É necessário fornecer filtros para excluir dados."
        return resultado
    
    try:
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()

        condicoes = " AND ".join([f"{col} = ?" for col in filtros.keys()])
        valores = tuple(filtros.values())

        sql = f"DELETE FROM {tabela} WHERE {condicoes}"
        cursor.execute(sql)
        conn.commit()
        conn.close()

        resultado["sucesso"] = True
        resultado["mensagem"] = f"{cursor.rowcount} registro(s) excluído(s) com sucesso."
    except Exception as e:
        resultado["mensagem"] = str(e)
    
    return resultado