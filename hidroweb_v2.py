# -*- coding: utf-8 -*-
 
"""
___________________________-> Python - Hidroweb <-______________________________
 
Autor: Arthur Alvin 25/04/2015
afmalvim@gmail.com
 
Modificação: Jean Favaretto 16/07/2015
jeanfavaretto@gmail.com
 
Modificação:Vitor Gustavo Geller 16/07/2015
vitorgg_hz@hotmail.com
 
______________________________-> Comentários <-_________________________________
 
O script Python HidroWeb foi criado  para automatizar o procedimento de aquisição 
de dados das estações do portal: http://hidroweb.ana.gov.br/
 
Para utilizar o script deverao ser instaladas as bibliotecas:
-> requests
-> beautifulsoup4 (ou superior)
 
UTILIZACAO:
    
Apos a instalacao das bibliotecas cria-se um Arquivo de Entrada, com o numero 
das estacoes. A proxima etapa será inicilizar o script, entao ele abrir uma
janela para selecionar o Arquivo de Entrada. Como saída o HidroWeb - Python, 
retorna duas informacoes. A primeira em tela, contendo a situacao do download. 
Por fim, gera-se no mesmo diretorio do Arquivo de Entrada, os arquivos de cada 
estacao que foi possivel realizar a transferencia (baixada).
 
 
ARQUIVO DE ENTRADA:
    
A entrada deve ser um arquivo *.txt contendo o número das estação a serem 
baixadas, com a seguinte estrutura:
-> O número das estacoes defem ser digitadas linhas apos linhas, 
sem cabecalhos, sem espacos, nem separadores (, . ;).
-> Simplismente um Enter após cada numero de estacao. 
 
02751025
02849035
02750004
02650032
02850015
 
 
SAIDAS:
 
Situação das transferencias em Tela:
** 02851050 **
** 02851050 ** (baixado)
** 02851050 ** (concluído)
 
No diretorio do Arquivo de Entrada serao criados os arquivos de saida contendo
a informacao disponivel de cada estacao baixada.
 
OBS: Tenha certeza que todos numeros das estacao existam, caso contrario da 
"BuuuG".
Palavras chave: HidroWeb, ANA, Estacoes, Pluviometricas, Fluviometricas,
Precipitacao, Vazao, Cotas, baixar, download. 
"""
 
# ********  DECLARACOES INICIAIS
import os
#import Tkinter, tkFileDialog
import sys
import requests
import re
import shutil
from bs4 import BeautifulSoup
 
# By Vitor
 
# ABRE ARQUIVO DE ENTRADA
#root    = Tkinter.Tk()
#entrada = tkFileDialog.askopenfile(mode='r')    
#root.destroy()
entrada = open("/root/teste/estacoes.txt")
 
#****************---------------correcao de bug--------------********************
if (entrada == None): 
    sair = raw_input('\tArquivo de entrada nao selecionado. \n\t\tPressione enter para sair.\n')
    sys.exit()
#****************---------------fim da correcao--------------********************
 
pathname = os.path.dirname(entrada.name) #define o path de trabalho igual ao do arquivo de entrada
os.chdir(pathname)  #muda caminho de trabalho.
 
VALORES = []
 
# By Jean
        
while True:
 
    conteudo_linha = entrada.read().split("\n")
    VALORES.append(conteudo_linha)
        
    if (len(conteudo_linha) <= 1):
        break
 
print VALORES, "\n"
 
 
#### By Arthur
 
class Hidroweb(object):
 
    url_estacao = 'http://hidroweb.ana.gov.br/Estacao.asp?Codigo={0}&CriaArq=true&TipoArq={1}'
    url_arquivo = 'http://hidroweb.ana.gov.br/{0}'
 
    def __init__(self, estacoes):
        self.estacoes = estacoes
 
    def montar_url_estacao(self, estacao, tipo=1):
        return self.url_estacao.format(estacao, tipo)
 
    def montar_url_arquivo(self, caminho):
        return self.url_arquivo.format(caminho)
 
    def montar_nome_arquivo(self, estacao):
        return u'{0}.zip'.format(estacao)
 
    def salvar_arquivo_texto(self, estacao, link):
        r = requests.get(self.montar_url_arquivo(link), stream=True)
        if r.status_code == 200:
            with open(self.montar_nome_arquivo(estacao), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print '** %s ** (baixado)' % (estacao, )
        else:
            print '** %s ** (problema)' % (estacao, )
 
    def obter_link_arquivo(self, response):
        soup = BeautifulSoup(response.content)
        return soup.find('a', href=re.compile('^ARQ/'))['href']
 
    def executar(self):
        post_data = {'cboTipoReg': '10'}
 
        for est in self.estacoes:
            print '** %s **' % (est, )
	    r = requests.post(self.montar_url_estacao(est), data=post_data)
#            print r.text 
#	    break
	    m = re.search("AVISO", r.text)
            if m:
	      print "Estacao "+est+" nao existe !"  
              continue	
    	    m = re.search("<p>Nenhum registro selecionado\.<\/p>", r.text)
            if m:
	      print "Estacao "+est+" sem dados !"  
              continue	
	    link = self.obter_link_arquivo(r)
            self.salvar_arquivo_texto(est, link)
            print '** %s ** (concluído)' % (est, )
 
if __name__ == '__main__':
    estacoes = VALORES[::1][0]
    hid = Hidroweb(estacoes)
    hid.executar()
