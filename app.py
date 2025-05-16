from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq(hl='pt-BR', tz=360)

@app.route('/trends')
def get_trends():
    termo = request.args.get('q', '')
    if not termo:
        return jsonify({"erro": "Palavra-chave (q) não fornecida"}), 400

    pytrends.build_payload([termo], cat=0, timeframe='now 7-d', geo='BR')
    dados = pytrends.interest_over_time()

    if dados.empty:
        return jsonify({"erro": "Sem dados para esse termo"}), 404

    resultado = dados[[termo]].reset_index().to_dict(orient='records')
    return jsonify(resultado)
