import pandas as pd
import matplotlib.pyplot as plt

# Configuração do estilo
plt.style.use('default')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
plt.rcParams['font.style'] = 'normal'
plt.rcParams["legend.framealpha"] = 1.0
plt.rcParams["savefig.dpi"] = 300

path_fluviogramas_obs = 'dados\originais\Fluviogramas_observados.csv'
path_fluviogramas_sim = 'dados\originais\Fluviogramas_simulados.csv'
df_fluv_obs = pd.read_csv(path_fluviogramas_obs)
df_fluv_sim = pd.read_csv(path_fluviogramas_sim)

datas_x_labels = ['1995-01-01', '2000-01-01', '2005-01-01', '2010-01-01', '2015-01-01']
anos = [1995, 2000, 2005, 2010, 2015]

# ESTAÇÃO: 38830000
campo_x = 'Data'
campo_y1 = '38830000'
campo_y2 = '1924'
plt.plot(df_fluv_obs[campo_x],
         df_fluv_obs[campo_y1],
         label='Observada')
plt.plot(df_fluv_sim[campo_x],
         df_fluv_sim[campo_y2],
         label='Simulada')
plt.xlabel('Data')
plt.ylabel('Vazão')
plt.title(f'Fluviograma Estação {campo_y1}')
plt.legend()
plt.grid(True)
plt.xticks(datas_x_labels, anos, rotation=45)
plt.savefig(f'graficos/fluviograma_observado_simulado_{campo_y1}.png')
plt.clf()
print('<<< FINALIZADO >>>')