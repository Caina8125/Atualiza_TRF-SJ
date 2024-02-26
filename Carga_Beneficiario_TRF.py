from src.Buscar_Relatorio_TRF import Buscar_Carteirinha
from src.Extrair_Dados_Pdf import Extrair_Dados
import menssage.Pidgin as pidgin
import API.Api_Amhptiss_hmg

def Iniciar_Atualizacao_Beneficiario():
    Buscar_Carteirinha()    


def Iniciar_Extracao_de_Dados():
    Extrair_Dados()

#-------------------------------------------------------------------

Iniciar_Atualizacao_Beneficiario()

Iniciar_Extracao_de_Dados()