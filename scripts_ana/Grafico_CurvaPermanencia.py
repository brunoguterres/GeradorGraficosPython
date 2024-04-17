# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:32:52 2024

@author: anamuhlenhoff
"""
## BIBLIOTECAS
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import locale

###############################################################################
#----------------------------- CÓDIGO PRINCIPAL ------------------------------#
###############################################################################
## Diretório de trabalho
os.chdir('//svrv2//Svrcuritiba//Tecnico//5411 - PRH Rio Paraíba//Ana//RP-03-DisponibilidadeHidrica//00_XLSX//00_Dados_Fluviometria')

## Configuração para exibir os meses em português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

## Definindo entradas:
estacoes = ['38830000', '38850000', '38860000', '38880000', '38895000']
cores = ['blue', 'purple', 'red', 'green', 'orange', 'dimgrey']
# ano_inicio = '1970'
# ano_fim = '2022'
inicio = pd.to_datetime('1970-01-01')
fim = pd.to_datetime('2022-12-31')


# Ler séries de dados das estações escolhidas
dt = pd.read_csv('SeriesCompletasEstacoes.csv', sep=';', header=0, 
                 usecols= ['Data'] + estacoes, na_values= -1, 
                 index_col= 'Data', parse_dates=['Data'])
dt = dt.loc[inicio:fim]

## Gera as curvas de permanencia e armazena em um dicionário
## {'código': DataFrame}
curva_permanencia = {}
for estacao in estacoes:
    serie = dt[estacao].dropna()
    serie_ordenada = serie.sort_values(ascending=False).values
    dto = pd.DataFrame(serie_ordenada, columns=[estacao])
    dto['Ordem'] = range(1, len(dto) + 1, 1)
    n = dto['Ordem'].max() + 1
    dto['Permanencia'] = (dto['Ordem']/n)*100
    dto.drop(columns=['Ordem'], inplace=True)
    curva_permanencia[estacao] = dto
    
### TABELA DAS PERMANÊNCIAS
qref = [98.0, 95.0, 90.0, 85.0, 80.0, 70.0, 75.0, 
        60.0, 50.0, 40.0, 30.0, 20.0, 15, 10.0]
perm = ['Q98%', 'Q95%', 'Q90%', 'Q85%', 'Q80%', 'Q70%', 'Q75%',
        'Q60%', 'Q50%', 'Q40%', 'Q30%', 'Q20%', 'Q15%', 'Q10%']

vazoes_ref = {}
for estacao in estacoes:
    df = curva_permanencia[estacao]
    lista_vazoes = []
    for q in qref:
        dif_abs = abs(df['Permanencia'] - q)
        p = dif_abs.idxmin()
        lista_vazoes.append(df.loc[p, estacao])
    vazoes_ref[estacao] = lista_vazoes
        
tabela_qref = pd.DataFrame(data=vazoes_ref)
tabela_qref['Qref'] = perm
tabela_qref.set_index('Qref', inplace=True)
tabela_qref = tabela_qref.reindex(index=tabela_qref.index[::-1])
tabela_qref.to_excel('VazoesDeReferencia.xlsx')


### GRÁFICO
# Estilo do gráfico
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 0.8
# Tamanho da figura
plt.rcParams["savefig.dpi"] = 150
largura = 17.9/2.54  # Converte para polegadas ( /2.54)
altura =  12/2.54  # Converte para polegadas ( /2.54)

## Plotando o gráfico
plt.figure(figsize=(largura, altura))
for estacao, cor in zip(estacoes, cores):
    df = curva_permanencia[estacao]
    x = df['Permanencia']
    y = df[estacao]
    plt.plot(x, y, linestyle='-', linewidth= 0.9, label= estacao, color= cor)

## Eixos
plt.xlabel('Permanência (%)')
plt.xlim(0, 100)
plt.xticks(ticks=range(0, 101, 10), labels=range(0, 101, 10))
plt.ylabel('Vazão (m³/s)')
plt.yscale("log")
plt.ylim(0.01, 2000)

# Editar formato dos números no eixo Y para usar vírgula como separador decimal
def format_func(value, tick_number):
    formatted_value = "{:,.2f}".format(value)
    formatted_value = formatted_value.replace(',', ';')
    return formatted_value.replace('.', ',').replace(';', '.')

# # Ajustar localizador de ticks para usar a mesma formatação
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_func))

plt.legend(loc='lower center', fontsize= 10, bbox_to_anchor=(0, -0.22, 1, 5),
              fancybox=True, ncol=5, mode='expand')
## Grid
plt.grid(True)
plt.grid(axis='both', which= 'major', linestyle='-', linewidth= 0.5, color='darkgrey')
plt.grid(axis='y', which= 'minor', linestyle='-', linewidth= 0.25, color='silver')
## Salvar figura
plt.savefig('CurvaPermanencia_LOG_final_2.png', bbox_inches='tight', pad_inches=0.1)
# plt.show()






































