import pandas as pd
import matplotlib.pyplot as plt

# Configuração do estilo
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["savefig.dpi"] = 500
plt.rcParams["lines.linewidth"] = 1

path_fluviogramas_obs = 'dados\originais\Fluviogramas_observados.csv'
path_fluviogramas_sim = 'dados\originais\Fluviogramas_simulados.csv'
df_fluv_obs = pd.read_csv(path_fluviogramas_obs)
df_fluv_sim = pd.read_csv(path_fluviogramas_sim)

# Filtrando os dados para o intervalo desejado
start_date = '2004-01-01'
end_date = '2012-12-31'
df_fluv_obs = df_fluv_obs[(df_fluv_obs['Data'] >= start_date) & (df_fluv_obs['Data'] <= end_date)]
df_fluv_sim = df_fluv_sim[(df_fluv_sim['Data'] >= start_date) & (df_fluv_sim['Data'] <= end_date)]

# ESTAÇÃO: 38830000
campo_x = 'Data'
campo_y1 = '38895000'
campo_y2 = '2039'
plt.plot(df_fluv_obs[campo_x],
         df_fluv_obs[campo_y1],
         label='Observada')
plt.plot(df_fluv_sim[campo_x],
         df_fluv_sim[campo_y2],
         label='Simulada')
plt.ylabel('Vazão')
plt.title(f'Estação {campo_y1}')
plt.grid(True)

# Definindo os rótulos desejados (apenas os anos)
rotulos = ['2004', '2008', '2012']
# Obtendo os índices dos pontos correspondentes nos dados
indices = [df_fluv_obs[df_fluv_obs[campo_x].str.startswith(r)].index[0] for r in rotulos]
# Ajustando os marcadores no eixo x
plt.xticks(df_fluv_obs[campo_x][indices], rotulos)

# Limitando a plotagem ao valor de 500 no eixo y
plt.ylim(0, 500)

# Salvando a figura
plt.savefig(f'graficos/fluviograma_observado_simulado_detalhe.png')
plt.clf()
print('<<< FINALIZADO >>>')
