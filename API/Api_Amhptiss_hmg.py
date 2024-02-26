import json
import time
import requests
import Authentication.Authentic
import numpy as np

def auth_hmg():
    global proxies

    urlAuth = 'https://hmg.amhp.com.br/api/Auth'

    proxies = {
        "http": f"http:// + {Authentication.Authentic.login_proxy}:{Authentication.Authentic.senha_proxy}@10.0.0.230:3128/",
        "https": f"http://{Authentication.Authentic.login_proxy}:{Authentication.Authentic.senha_proxy}@10.0.0.230:3128/"
    }

    usuario_login = {
        "Usuario": Authentication.Authentic.login_censo,
        "Senha" : Authentication.Authentic.senha_censo
    }

    post = requests.post(urlAuth, usuario_login, proxies=proxies)
    time.sleep(1)
    content = json.loads(post.content)
    time.sleep(1)
    token = content['AccessToken']
    print("")
    print('Token =>',token)
    print("")

    return token


def Enviar_lista_beneficiario(token, lista,convenio):
    urlPost = f"http://localhost:33000/api/upload-beneficiarios"

    headers = {
        'Authorization': f'Bearer {token}'
    }

    lista_de_dicionarios = []
    for i in lista:
        dados = {
            "Id": 0,
            "NumeroCartao": i[1],
            "NumeroCartaoNacional": "",
            "NomePlano": "",
            "Nome": i[4],
            "Sexo": "",
            "Nascimento": "",
            "Falecimento": "",
            "InicioPlano": "",
            "FimPlano": "",
            "EmissaoCarteira": "",
            "Validade": "",
            "NomeTitular": "",
            "PessoaInclusao": 0,
            "PessoaAlteracao": 0,
            "DataInclusao": "",
            "DataAlteracao": "",
            "Operadora": convenio,
            "Origem": 0
        }

        lista_de_dicionarios.append(dados)

    data = lista_de_dicionarios
    qtd = len(data)
    print(data)
    response = requests.post(urlPost, headers=headers, json=data, verify=False)
    print("")
    print(response)
    print("")
    content = json.loads(response.content)
    print("")
    print(content)

    return qtd