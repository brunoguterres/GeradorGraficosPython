# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 10:38:24 2024
@author: anamuhlenhoff

Código para criar um g´rafico de barras para a vazão média mensal de longo termo 
para uma lista de estações.
Formato do gráfico está para 5 estações.

Estações fluviométricas no rio Paraíba:
    ['38830000', '38860000', '38880000', '38895000']

Estações fluviométricas no rio Taperoá:
    ['38850000']
    
"""
## BIBLIOTECAS
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale

def limpa_dados(df): 
    for coluna in df:
        df[coluna] = df[coluna].str.replace('*', '')
        df[coluna] = df[coluna].str.replace('?', '')
        df[coluna] = df[coluna].str.replace('#', '')
        df[coluna] = df[coluna].str.replace(',', '.')
        df[coluna] = df[coluna].astype(float)
    return df

def df_melted(df):
    df = df.rename(columns={'Jan': '1', 'Fev': '2', 'Mar': '3', 'Abr': '4',
                            'Mai': '5', 'Jun': '6', 'Jul': '7', 'Ago': '8',
                            'Set': '9', 'Out':'10', 'Nov':'11', 'Dez':'12'})
    df.reset_index(inplace=True)                                                # Resetando o índice para que o ano se torne uma coluna
    df = df.melt(id_vars=['Ano'], var_name='Mês', value_name='Vazão')  # Derretendo o DataFrame para reorganizar os dados em três colunas: ano, mês e valor
    df['Mês'] = df['Mês'].astype(int)
    
    datas = []
    for row in df.index:
        ano = int(df['Ano'][row])
        mes = int(df['Mês'][row])
        data = datetime(ano, mes, 1)
        datas.append(data)
        
    df['Data'] = datas
    df = df.sort_values(by='Data', ascending=True)
    df = df.set_index('Data')
    
    return df

def le_serie_consistida(arquivo, melted = True, skipfooter = 3):
    ## Leitura de dados consistidos
    consistido = pd.read_excel(arquivo, sheet_name='Consistido', 
                               dtype=str, header= 6, index_col='Ano',
                               usecols=lambda x: x != 'Média',
                               skipfooter= skipfooter)
    consistido = limpa_dados(consistido)
    
    if melted == True: 
        consistido = df_melted(consistido)
        return consistido
    else:    
        return consistido

def le_serie_bruta(arquivo, melted = True, skipfooter = 3):
    ## Leitura de dados brutos
    bruto = pd.read_excel(arquivo, sheet_name='Bruto', 
                          dtype=str, header= 6, index_col='Ano',
                          usecols=lambda x: x != 'Média',
                          skipfooter= skipfooter)
    bruto = limpa_dados(bruto)
    
    if melted == True: 
        bruto = df_melted(bruto)
        return bruto
    else:
        return bruto

def qmlt_mensal(estacoes, cores, ano_inicio, ano_fim, save = True):
    
    medias = pd.DataFrame()
    for i, estacao in enumerate(estacoes):
        arquivo = 'VazaoMedia_' + estacao + '.xlsx'
        dc = le_serie_consistida(arquivo, melted= False, skipfooter= 3)
        db = le_serie_bruta(arquivo, melted= False, skipfooter= 3)
        df = pd.concat([dc, db], axis= 0)
        df = df.loc[ano_inicio:ano_fim]
        aux = df.mean(axis=0)
        aux = pd.DataFrame(aux, columns=[estacao])
        medias = pd.concat([medias, aux], axis= 1)
    
    ## Gráfico vazão média mensal de longo termo para cada estação
    # Estilo do gráfico
    plt.style.use('default')
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.style'] = 'normal'
    plt.rcParams["legend.framealpha"] = 0.8
    # Tamanho da figura
    plt.rcParams["savefig.dpi"] = 300
    largura = 18.2/2.54  # Converte para polegadas ( /2.54)
    altura =  6/2.54  # Converte para polegadas ( /2.54)
    
    # Vazão média de longo termo para o período de 1970 a 2022
    ax = medias.plot(kind='bar',  figsize=(largura, altura), color = cores,
                     zorder=1)
    plt.ylabel('Vazão média (m³/s)')
    xticks_pos = range(len(medias.index))
    plt.xticks(xticks_pos, medias.index, rotation=0, minor=True)
    ax.set_xticks([p + 0.5 for p in xticks_pos], minor=False) 
    plt.legend(loc = 'lower center', ncol= 5, 
               bbox_to_anchor= (0, -0.25, 1, 4), fancybox= True, frameon= True,
               mode= 'expand', borderaxespad = 0, handletextpad=0.2)
    plt.grid(True, linestyle='-', linewidth=0.3, color='silver', 
             axis='both', zorder=0)
    
    if save == True: 
        plt.savefig('Qmlt_estacoes_ok.png', bbox_inches='tight', pad_inches=0.1)
    else:
        plt.show()
        
    return

###############################################################################
#----------------------------- CÓDIGO PRINCIPAL ------------------------------#
###############################################################################
## Diretório de trabalho
os.chdir('//svrv2//Svrcuritiba//Tecnico//5411 - PRH Rio Paraíba//Ana//RP-03-DisponibilidadeHidrica//00_XLSX//00_Dados_Fluviometria')

## Configuração para exibir os meses em português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

## Definindo entradas:
estacoes = ['38830000', '38850000', '38860000', '38880000', '38895000']
cores = ['navy', 'purple', 'red', 'green', 'orange', 'dimgrey']
ano_inicio = '1970'
ano_fim = '2022'

## Chamando a função para criar o gráfico
qmlt_mensal(estacoes, cores, ano_inicio, ano_fim, save = True)

