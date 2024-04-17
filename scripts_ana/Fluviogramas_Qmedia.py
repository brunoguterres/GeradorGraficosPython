# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:01:47 2024
@author: anamuhlenhoff

Fluviograma de vazões médias
Exemplo de arquivo de entrada para as funções de leitura: 'VazaoMedia_38830000.xlsx'
Formato de arquivo > vazões médias obtidas do HIDRO
"""

## BIBLIOTECAS
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import locale

# Configuração para exibir os meses em português
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

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

def le_serie_consistida(arquivo):
    ## Leitura de dados consistidos
    consistido = pd.read_excel(arquivo, sheet_name='Consistido', 
                               dtype=str, header= 6, index_col='Ano',
                               usecols=lambda x: x != 'Média',
                               skipfooter= 3)
    consistido = limpa_dados(consistido)
    consistido = df_melted(consistido)
    return consistido

def le_serie_bruta(arquivo):
    ## Leitura de dados brutos
    bruto = pd.read_excel(arquivo, sheet_name='Bruto', 
                          dtype=str, header= 6, index_col='Ano',
                          usecols=lambda x: x != 'Média',
                          skipfooter= 3)
    bruto = limpa_dados(bruto)
    bruto = df_melted(bruto)
    return bruto

def fluviograma(arquivo, estacao, inicio, fim, save= False):
    ## Cópia dos dados para o gráfico
    dc = le_serie_consistida(arquivo)
    db = le_serie_bruta(arquivo)
    df = pd.concat([dc, db], axis=0)
    
    # Recorte do período de interesse
    df = df.loc[inicio:fim]
    
    # Rótulos do eixo x - todos os janeiros mais a data inicial e a data final
    aux = df[df.index.month == 1].index.tolist()
    auxr = []
    for i in range(0, len(aux), 3):
        auxr.append(aux[i])
    rotulos = [df.index[0]] + auxr + [df.index[-1]]
    rotulos = np.asarray(rotulos)
    
    # Estilo
    plt.style.use('default')
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 10
    plt.rcParams['font.style'] = 'normal'
    plt.rcParams["legend.framealpha"] = 1.0
    plt.rcParams["savefig.dpi"] = 300
    
    # Plotando o gráfico
    plt.figure(figsize=(18.2/2.54, 6/2.54))
    plt.plot(df.index, df['Vazão'], linestyle='-', linewidth= 0.5,
             label= estacao, color='navy')

    
    # Eixo x
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
    plt.xlim(df.index[0],df.index[-1])
    plt.xticks(ticks=rotulos, rotation=90)
    # plt.gca().xaxis.set_major_locator(plt.MaxNLocator(45))
    
    # Título do gráfico, título eixo y, legenda, grid
    # plt.title('Estação Fluviométrica ' + estacao)
    plt.ylabel('Vazão média (m³/s)')
    plt.legend(loc= 'upper right', fontsize= 10)
    plt.grid(True)
    plt.grid(linestyle='-', linewidth=0.3, color='silver', axis='both')
    
    if save == True: 
        figname = estacao + '_Fluviograma.png'
        plt.savefig(fname= figname, bbox_inches='tight', pad_inches=0.1)
    
    elif save == False:
        plt.show()
    
    return

###############################################################################
#----------------------------- CÓDIGO PRINCIPAL ------------------------------#
###############################################################################
## Diretório de trabalho
os.chdir('//svrv2//Svrcuritiba//Tecnico//5411 - PRH Rio Paraíba//Ana//RP-03-DisponibilidadeHidrica//00_XLSX//00_Dados_Fluviometria')

estflu_rio_paraiba = ['38830000', '38860000', '38880000', '38895000', '38850000']
estflu_rio_taperoa = ['38850000']
cores = ['navy', 'red', 'green', 'orange', 'purple']

data_inicio = pd.to_datetime('1970-01-01')
data_fim = pd.to_datetime('2022-12-01')
estacoes = estflu_rio_paraiba
# ## Teste fluviograma
# arquivo = 'VazaoMedia_38830000.xlsx'
# estacao = '38830000'
# fluviograma(arquivo, estacao, data_inicio, data_fim, save=True)

# ## Plotar para todas as estações no rio Paraiba
# for estacao in estflu_rio_paraiba:
#     arquivo = 'VazaoMedia_' + estacao + '.xlsx'
#     fluviograma(arquivo, estacao, data_inicio, data_fim, save=True)


## Cópia dos dados para o gráfico HIDROGRAMA SIMULTÂNEO
dt = pd.DataFrame()
for estacao in estflu_rio_paraiba:
    arquivo = 'VazaoMedia_' + estacao + '.xlsx'
    dc = le_serie_consistida(arquivo)
    db = le_serie_bruta(arquivo)
    df = pd.concat([dc, db], axis=0)
    df.rename(columns={'Vazão': estacao}, inplace=True)
    dt = pd.concat([dt, df[estacao]], axis=1)
dt = dt.sort_index()
dt = dt.loc[data_inicio:data_fim]
dt.to_excel('SeriesMensaisMaximos.xlsx', index=True)

# Definindo os intervalos para o eixo x nos subplots
t0 = []; tf = []
for i in range(0, len(dt.index), 106):
    inicio = pd.to_datetime(dt.index[i])
    fim = pd.to_datetime(dt.index[i-1])
    t0.append(inicio)
    tf.append(fim)
t0 = sorted(t0)
tf = sorted(tf)

# Definindo altura, largura e as margens da figura em polegadas
largura = 17.88/2.54
altura = 24.7/2.54
left_margin = 1.4  # Margem esquerda
right_margin = 1  # Margem direita
bottom_margin = 1  # Margem inferior
top_margin = 1  # Margem superior

# Estilo do gráfico
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["savefig.dpi"] = 150

# Plotando os fluviogramas
fig, axs = plt.subplots(6, 1, figsize= (largura, altura), sharex=False, sharey=False,
                        gridspec_kw={'hspace': 0.3, 'top': 0.95})
fig.subplots_adjust(left=left_margin/10, 
                    right=1-right_margin/10, 
                    bottom=bottom_margin/10, 
                    top=1-top_margin/10)
fig.text(0.05, 0.5, 'Vazão média (m³/s)', va='center', rotation='vertical')  # Título do eixo y comum para todos os subplots

indice = range(0,6,1)
for i in indice:
    data_inicio = t0[i]
    data_fim = tf[i]
    dados = dt.loc[data_inicio:data_fim]
    for k, estacao in enumerate(estacoes):
        axs[i].plot(dados.index, dados[estacao], linestyle='-', linewidth=0.9,
                    label= estacao, color= cores[k])
        # Eixo x
        axs[i].set_xlim(data_inicio, data_fim)
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
        axs[i].grid(True, linestyle='-', linewidth=0.5, color='silver', axis='both')
        
axs[i].legend(loc='lower center', fontsize= 10, bbox_to_anchor=(0, -0.65, 1, 4),
              fancybox=True, ncol=5, mode='expand')

plt.savefig(fname= 'Fluviograma_Simultaneo1.png', bbox_inches='tight', pad_inches=0.1)


