# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 13:53:21 2024

@author: anamuhlenhoff
"""

## BIBLIOTECAS
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import locale

def limpa_dados(df): 
    for coluna in df:
        df[coluna] = df[coluna].str.replace('*', '')
        df[coluna] = df[coluna].str.replace('?', '')
        df[coluna] = df[coluna].str.replace('#', '')
        df[coluna] = df[coluna].str.replace(',', '.')
        df[coluna] = df[coluna].astype(float)
    return df

###############################################################################
#----------------------------- CÓDIGO PRINCIPAL ------------------------------#
###############################################################################
## Diretório de trabalho
os.chdir('//svrv2//Svrcuritiba//Tecnico//5411 - PRH Rio Paraíba//Ana//RP-03-DisponibilidadeHidrica//00_XLSX//00_Dados_Fluviometria')

estacoes = ['38830000', '38850000', '38860000', '38880000', '38895000']
# cores = ['blue', 'red', 'green', 'orange', 'purple', 'dimgrey']
# ano_inicio = '1970'
# ano_fim = '2022'
# inicio = pd.to_datetime('1970-01-01')
# fim = pd.to_datetime('2022-12-31')

medias_anuais = {}
for estacao in estacoes:
    ## Nome do arquivo com os dados
    arquivo = 'VazaoMedia_' + estacao + '.xlsx'
    
    ## Leitura de dados consistidos e brutos
    dc = pd.read_excel(arquivo, sheet_name='Consistido', dtype=str, header= 6, 
                       usecols=['Ano', 'Média'], skipfooter= 3)
    db = pd.read_excel(arquivo, sheet_name='Bruto', dtype=str, header= 6, 
                       usecols=['Ano', 'Média'], skipfooter= 3)
    
    ## Organizando os dados
    df = pd.concat([dc, db], axis=0)
    df = df.rename(columns={'Média': estacao})
    df.sort_values(by='Ano', ascending=True)
    df.set_index('Ano', inplace=True)
    df = limpa_dados(df)
    medias_anuais[estacao] = df

df = medias_anuais[estacoes[0]]
for estacao in estacoes[1:]:
    d1 = medias_anuais[estacao]
    df = pd.concat([df, d1], axis=1)
df = df.sort_index()    

### GRÁFICO
# Estilo do gráfico
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 1
# Tamanho da figura
plt.rcParams["savefig.dpi"] = 150
largura = 17.9/2.54  # Converte para polegadas ( /2.54)
altura =  12/2.54  # Converte para polegadas ( /2.54)

## Plotando o gráfico
plt.figure(figsize=(largura, altura))
df.boxplot(patch_artist=True,  # Preencher os retângulos
           boxprops=dict(facecolor='gainsboro', linewidth=0.5),  # Propriedades da caixa
           medianprops=dict(color='navy', linewidth= 1.5, label='Mediana'),      # Propriedades da mediana
           whiskerprops=dict(color='black', linewidth=1),       # Propriedades dos bigodes
           capprops=dict(color='black', linewidth=1),        # Propriedades das extremidades dos bigodes
           meanprops=dict(marker='D', markerfacecolor='red', markeredgecolor='black', markersize=15),  # Propriedades da média
           flierprops=dict(marker='x', markeredgecolor='red', markersize=4))  # Propriedades dos outliers
plt.ylabel('Vazão média anual (m³/s)')
plt.xlabel('Estações Fluviométricas')
median_color = 'navy'  # Cor da mediana
median_marker = '_'     # Marcador da mediana (traço)
plt.legend([plt.Line2D([0], [0], marker=median_marker, color=median_color, markersize=10, linestyle='-',linewidth=1.5)],
           ['Mediana'], loc='upper right')
## Salvar figura
plt.savefig('BoxPlotsVazoesAnuais_estacoes.png', bbox_inches='tight', pad_inches=0.1)
# plt.show()
