from flask import Blueprint, render_template, current_app
from .tabela_price import calcular_tabela_price

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Pass the flag from app config to the template.
    return render_template(
        'index.html',
        show_table=current_app.config.get('SHOW_TABLE', False),
        config_interest=current_app.config.get('JUROS', 15.0)
    )

@main.route('/calcular', methods=['POST'])
def calcular():
    from flask import request, jsonify
    dados = request.get_json()
    try:
        principal = float(dados.get('principal', 0))
        # Get the interest rate from configuration (in percent) and convert to decimal:
        taxa_percentual = current_app.config.get('JUROS', 15.0)
        meses = int(dados.get('meses', 0))
        taxa_mensal = taxa_percentual / 100
        tabela = calcular_tabela_price(principal, taxa_mensal, meses)
        return jsonify({"tabela": tabela})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
