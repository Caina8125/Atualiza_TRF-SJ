from PyPDF2 import PdfReader
import re
import pandas as pd
import csv
import API.Api_Amhptiss as Api_Amhptiss
import menssage.Telegram as telegram
import menssage.Pidgin as pidgin


def removeAll(texto, frases_a_excluir):
    novo_texto = texto.replace(frases_a_excluir,"")
    return novo_texto

def remover_frase_iniciada_com(texto, palavra):
    padrao = fr'\b{palavra}\b.*?[\.\?!]'
    novo_texto = re.sub(padrao, '', texto)
    # print(novo_texto)
    return novo_texto

def quebrar_texto(texto):
    novo_texto = texto.split("\n")
    lista_split = [item.split("   ") for item in novo_texto]
    # lista_split.append(carteirinha)
    return lista_split

def extrair_carteirinha(texto):
    numeros = re.findall(r'\d+', texto)
    numeros = [numero for numero in numeros if len(numero) >= 15]
    # print(numeros)
    return numeros

def remover_numeros(texto):
    texto_sem_numeros = re.sub(r'\d+', ' ', texto)
    # print(texto_sem_numeros)
    return texto_sem_numeros

def gerar_dataFrame(matriz, carteirinha, header):
    tabela = pd.DataFrame(matriz, columns=header)
    tabela = tabela.dropna()
    nova_coluna = carteirinha
    tabela['NumeroCartao'] = nova_coluna

    tabela = tabela.reindex(['Id','NumeroCartao', 'NumeroCartaoNacional',
                             'NomePlano', 'Nome', 'Convênio', 'sexo',
                             'Nascimento', 'Falecimento', 'InicioPlano',
                             'FimPlano', 'EmissaoCarteira', 'Validade',
                             'NomeTitular','PessoaInclusao', 'PessoaAlteracao',
                             'DataInclusao', 'DataAlteracao','Operadora',
                             'Origem'
                             ], axis=1)
    
    # print(tabela)
    return tabela


def gerar_arquivo(df):
    sj_trf = df[df['Convênio'] == "Seção Judiciária do Distrito Federal"]
    sj_trf = sj_trf.drop('Convênio', axis=1)

    trf = df[df['Convênio'] != "Seção Judiciária do Distrito Federal"]
    trf = trf.drop('Convênio', axis=1)

    sj_trf.to_csv(r'Doc/SJ_TRF.csv', header=False, index=False, encoding='utf-16', sep=';')
    trf.to_csv(r'Doc/TRF.csv', header=False, index=False, encoding='utf-16', sep=';')

def extrair_TRF(df):
    trf = df[df['Convênio'] != "Seção Judiciária do Distrito Federal"]
    trf = trf.drop('Convênio', axis=1)
    trf = trf.values.tolist()

    return trf

def extrair_SJ(df):
    sj_trf = df[df['Convênio'] == "Seção Judiciária do Distrito Federal"]
    sj_trf = sj_trf.drop('Convênio', axis=1)
    sj_trf = sj_trf.values.tolist()

    return sj_trf

#-----------------------------------------------------------------------------------------------------------------------------------

def Extrair_Dados():
    # Abrindo um arquivo PDF existente
    # with open(r"C:\PDF_TRF_SJ\reportdownload.pdf", "rb") as input_pdf:

    header = ("Convênio", "Nome")
    i = 0
    convenio_trf = 25201
    convenio_sj = 25155
    df = pd.DataFrame()

    # Criando um objeto PdfFileReader
    pdf_reader = PdfReader(r"C:\PDF_TRF_SJ\reportdownload.pdf")

    # Obtendo o número de páginas do arquivo PDF
    num_pages = len(pdf_reader.pages)

    # Lendo o texto de cada página
    for page_number in range(num_pages):
        i += 1
        page = pdf_reader.pages[page_number]

        text = page.extract_text()

        novo_texto = removeAll(text, 'Programa de Assistência aos Magistrados e Servidores da Justiça Federal de 1º')
        novo_texto = removeAll(novo_texto, ' e 2º Graus da 1ª Região.')
        novo_texto = removeAll(novo_texto, 'TRF115 - Listagem de Beneficiários')
        novo_texto = removeAll(novo_texto, ' Lotação Cartão Nome do Beneficiário')
        novo_texto = removeAll(novo_texto, f' {i} 00735860000173')
        novo_texto = removeAll(novo_texto, 'Antes de imprimir, avalie seu compromisso com o MEIO AMBIENTE e seu comprometimento com os CUSTOS')
        novo_texto = remover_frase_iniciada_com(novo_texto, f'Sistema ')

        carteirinha = extrair_carteirinha(novo_texto)

        texto_sem_numero = remover_numeros(novo_texto)

        separacao = quebrar_texto(texto_sem_numero)

        tabela = gerar_dataFrame(separacao, carteirinha, header)

        df = df.append(tabela, ignore_index=True)
        print(df)
        
    sj = extrair_SJ(df)

    trf = extrair_TRF(df)
    
    token = Api_Amhptiss.auth()

    try:
        post_Sj = Api_Amhptiss.Enviar_lista_beneficiario(token,sj,convenio_sj)
        telegram.Amhp(f"{post_Sj}  Beneficiários do SJ-DF atualizados no AMHPTISS")
    except Exception as e:
        telegram.Dev(f"Erro ao enviar a lista de Beneficiarios do TRF para a API. {e.__class__.__name__}: {e}")
    
    try:
        post_Trf = Api_Amhptiss.Enviar_lista_beneficiario(token,trf,convenio_trf)
        telegram.Amhp(f"{post_Trf}  Beneficiários do TRF atualizados no AMHPTISS")
    except Exception as e:
        telegram.Dev(f"Erro ao enviar a lista de Beneficiarios do SJ para a API. {e.__class__.__name__}: {e}")


    