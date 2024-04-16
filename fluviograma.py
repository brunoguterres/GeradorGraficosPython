import pandas as pd
import matplotlib.pyplot as plt

path_fluviogramas_obs = 'dados\originais\Fluviogramas_observados_teste.csv'
path_fluviogramas_sim = 'dados\originais\Fluviogramas_simulados_teste.csv'
df_fluv_obs = pd.read_csv(path_fluviogramas_obs)
df_fluv_sim = pd.read_csv(path_fluviogramas_sim)

print(df_fluv_obs.head())
print(df_fluv_sim.head())

matriz_fluv_obs = df_fluv_obs.values
matriz_fluv_sim = df_fluv_sim.values


# ESTAÇÃO: 38830000

campo_x = 'Data'
campo_y1 = '38830000'
campo_y2 = '1924'

plt.plot(df_fluv_obs[campo_x], df_fluv_obs[campo_y1], label='Observada')
plt.plot(df_fluv_sim[campo_x], df_fluv_sim[campo_y2], label='Simulada')
plt.xlabel('Data')
plt.ylabel('Vazão')
plt.title(f'Fluviograma (observado/simulado) - Estação {campo_y1}')
plt.legend()
plt.grid(False)

plt.savefig(f'fluviograma_observado_simulado_{campo_y1}.png')

plt.clf()