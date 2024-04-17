import pandas as pd
import matplotlib.pyplot as plt
import time

tempo_inicial = time.time()

path_fluviogramas_obs = 'dados\originais\Fluviogramas_observados.csv'
path_fluviogramas_sim = 'dados\originais\Fluviogramas_simulados 1.csv'
df_fluv_obs = pd.read_csv(path_fluviogramas_obs)
df_fluv_sim = pd.read_csv(path_fluviogramas_sim)

datas_x_labels = ['1995-01-01', '2000-01-01', '2005-01-01', '2010-01-01', '2015-01-01']

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
plt.title(f'Fluviograma (observado/simulado) - Estação {campo_y1}')
plt.legend()
plt.grid(True)

tempo_final = time.time()
print(f'tempo de execução: {tempo_final-tempo_inicial:.1f}s')

plt.xticks(datas_x_labels, rotation=45)
plt.show()

#plt.savefig(f'fluviograma_observado_simulado_{campo_y1}.png')
#plt.clf()