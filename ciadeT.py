import re
import requests
from scrapy import Selector

# Termos e padrões para identificar vagas da área de TI
PALAVRAS_CHAVE_TI = [
    r'\bti\b',
    r'\bt\.i\.?\b',
    r'tecnologia da informa[çc][ãa]o',
    r'cursos? de tecnologia',
    r'ci[êe]ncia da computa[çc][ãa]o',
    r'engenharia (?:de|da) computa[çc][ãa]o',
    r'engenharia de software',
    r'sistemas de informa[çc][ãa]o',
    r'an[áa]lise (?:e desenvolvimento )?de sistemas',
    r'\bcomputa[çc][ãa]o\b',
    r'\binform[áa]tica\b',
    r'desenvolv(?:edor|imento de software)',
    r'\bsoftware\b',
    r'\bprogramador\b',
    r'\bprograma[çc][ãa]o\b',
    r'\bdeveloper\b',
    r'\bdevs?\b',
    r'banco de dados',
    r'ci[êe]ncia de dados',
    r'data science',
    r'analista de dados',
    r'engenheir[oa] de dados',
    r'seguran[çc]a da informa[çc][ãa]o',
    r'ciberseguran[çc]a',
    r'cybersecurity',
    r'cloud computing',
    r'\bdevops\b',
    r'front-?end',
    r'back-?end',
    r'full-?stack',
    r'\btech\b',
]

PADRAO_TI = re.compile('|'.join(PALAVRAS_CHAVE_TI), re.IGNORECASE)

def eh_vaga_ti(texto: str) -> bool:
    return bool(PADRAO_TI.search(texto))

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

json_data = {
    'locale': 'pt',
}

response = requests.post(
    'https://vagas.ciadetalentos.com.br/applicant/rest/applicant/authentication/filter',
    headers=headers,
    json=json_data,
)

dados = response.json()

url = 'https://www.ciadeestagios.com.br/vagas-de-estagio/#vagas'

html = requests.get(url).content

response = Selector(text = html)

links = response.css('a.button.button--green.button--md.button--full-width::attr(href)').getall()

for link in links:
    try:
        conteudo_pagina = requests.get(link, timeout=10).content.decode('utf-8', errors='ignore')
        if eh_vaga_ti(conteudo_pagina):
            with open('vagas.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(link + '\n')
    except requests.RequestException:
        pass

for vaga in dados:
    nome_vaga = vaga['opportunityName']
    local_vaga = vaga['opportunityLocations']
    area_vaga = vaga['opportunityAreas']
    empresa_vaga = vaga['companyName']
    tempo = vaga['daysRemainingForInscription']
    descricao = vaga.get('opportunityDescription', '')

    texto_completo = f"{nome_vaga} {area_vaga} {descricao}"

    if eh_vaga_ti(texto_completo):
        with open('vagas.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"{nome_vaga}\n{local_vaga}\n{area_vaga.replace('Área','Area')}\n{empresa_vaga}\n{tempo}\n\n")
