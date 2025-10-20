
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/criar-banco")
def criar_banco():
    resultado = criar_banco_e_tabelas(db_structure)
    return jsonify(resultado)  # Retorna o resultado para o front em JSON
breakpoint()
if __name__ == "__main__":
    app.run(debug=True)

# Pausa a execução até que o usuário pressione Enter
input("Pressione Enter para continuar...")