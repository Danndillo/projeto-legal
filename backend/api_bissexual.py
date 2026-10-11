from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/api/vagas', methods=['GET', 'POST'])
def get_estagios_data():
    url = 'https://vagas.ciadetalentos.com.br/applicant/rest/applicant/authentication/filter'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://www.ciadetalentos.com.br',
        'priority': 'u=1, i',
        'referer': 'https://www.ciadetalentos.com.br/',
        'sec-ch-ua': '"Chromium";v="154", "Google Chrome";v="154", "Not A(Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
    }

    json = {
        'locale': 'pt',
    }

    response =requests.post(url, headers=headers, json=json)

    if response.status_code == 200:
        data = response.json();
        return data
    else:
        return None

@app.route('/api/teste')
def teste_cia_estagio():
    url = 'https://sgce.ciadeestagios.com.br/api/listar.vagas.publicas'
    r = requests.get(url)
    
    return jsonify({
        'status': r.status_code,
        'data': r.json() if r.headers.get('content-type', '').startswith('application/json') else r.text[:500]
    })

if __name__ == '__main__':
    app.run()