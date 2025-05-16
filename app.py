from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
headers = {'User-Agent': 'Mozilla/5.0'}
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
        import traceback
        print("Erro ao buscar:", termo)
        print(traceback.format_exc())
        return jsonify({"erro": str(e)}), 500

