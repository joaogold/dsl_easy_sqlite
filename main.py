
from flask import Flask, render_template, jsonify

app = Flask(__name__)

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

adicionar_dados("meu_banco.db", "usuarios", {
    "nome": "João",
    "email": "joao@email.com",
    "idade": 25
})

pesquisar_dados("meu_banco.db", "usuarios", {"idade": 25})

excluir_dados("meu_banco.db", "usuarios", {"nome": "João"})

@app.route("/criar-banco")
def criar_banco():
    resultado = criar_banco_e_tabelas(db_structure)
    return jsonify(resultado)  # Retorna o resultado para o front em JSON

@app.route("/adicionar", methods=["POST"])
def adicionar():
    dados = request.json
    resultado = adicionar_dados(dados["banco"], dados["tabela"], dados["valores"])
    return jsonify(resultado)

@app.route("/pesquisar", methods=["POST"])
def pesquisar():
    dados = request.json
    resultados = pesquisar_dados(dados["banco"], dados["tabela"], dados.get("filtros"))
    return jsonify({"resultados": resultados})

@app.route("/excluir", methods=["POST"])
def excluir():
    dados = request.json
    resultado = excluir_dados(dados["banco"], dados["tabela"], dados["filtros"])
    return jsonify(resultado)

breakpoint()

if __name__ == "__main__":
    app.run(debug=True)

# Pausa a execução até que o usuário pressione Enter
input("Pressione Enter para continuar...")