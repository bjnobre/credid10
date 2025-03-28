from flask import Blueprint, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Use the app's configured static folder
    return current_app.send_static_file('index.html')

@main.route('/calcular', methods=['POST'])
def calcular():
    # Your calculation logic here...
    from flask import request, jsonify
    from .tabela_price import calcular_tabela_price

    dados = request.get_json()
    try:
        principal = float(dados.get('principal', 0))
        taxa_percentual = float(dados.get('juros', 0))
        meses = int(dados.get('meses', 0))
        taxa_mensal = taxa_percentual / 100
        tabela = calcular_tabela_price(principal, taxa_mensal, meses)
        return jsonify({"tabela": tabela})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
