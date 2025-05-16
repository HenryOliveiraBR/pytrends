from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'}
pytrends = TrendReq(hl='pt-BR', tz=360, requests_args={'headers': headers})


@app.route('/trends')
def get_trends():
    termo = request.args.get('q')
    if not termo:
        return jsonify({"erro": "É necessário passar o parâmetro 'q'"}), 400

    try:
        pytrends.build_payload([termo], timeframe='now 7-d', geo='BR')
        df = pytrends.interest_over_time()
        if df.empty:
            return jsonify([])

        resultados = []
        for index, row in df.iterrows():
            resultados.append([index.strftime('%Y-%m-%d'), int(row[termo])])

        return jsonify(resultados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
