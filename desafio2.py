from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

#Criar banco de dados SQLite para armazenar endereços
def criar_tabela():
    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cep TEXT UNIQUE,
            logradouro TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela()

#Função para consultar o CEP na API ViaCEP
def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    return resposta.json() if resposta.status_code == 200 else None

#Rota para buscar um endereço e armazenar no banco
@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.json
    cep = dados.get("cep")

    if not cep or len(cep) != 8:
        return jsonify({"erro": "CEP inválido!"}), 400

    endereco = buscar_cep(cep)

    if not endereco or "erro" in endereco:
        return jsonify({"erro": "CEP não encontrado!"}), 404

    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR IGNORE INTO enderecos (cep, logradouro, bairro, cidade, estado) VALUES (?, ?, ?, ?, ?)",
        (cep, endereco.get("logradouro"), endereco.get("bairro"), endereco.get("localidade"), endereco.get("uf")),
    )
    
    conn.commit()
    conn.close()
    
    return jsonify(endereco)

#Rota para listar os endereços salvos com opção de ordenação
@app.route("/enderecos", methods=["GET"])
def listar():
    ordenacao = request.args.get("ordenar_por", "cidade")  # Padrão: ordenar por cidade

    if ordenacao not in ["cidade", "bairro", "estado"]:
        return jsonify({"erro": "Parâmetro de ordenação inválido!"}), 400

    conn = sqlite3.connect("enderecos.db")
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM enderecos ORDER BY {ordenacao} ASC")
    enderecos = cursor.fetchall()
    conn.close()

    return jsonify([{"cep": e[1], "logradouro": e[2], "bairro": e[3], "cidade": e[4], "estado": e[5]} for e in enderecos])

if __name__ == "__main__":
    app.run(debug=True)
