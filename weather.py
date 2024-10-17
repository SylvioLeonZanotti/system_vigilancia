import requests

def obter_dados_clima(api_key, cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        temperatura = dados['main']['temp']
        umidade = dados['main']['humidity']
        condicao = dados['weather'][0]['description']
        return temperatura, umidade, condicao
    else:
        print(f"Erro ao obter dados de clima: {response.status_code}")
        return None, None, None