import pandas as pd
import matplotlib.pyplot as plt

path_fluviogramas_obs = 'dados\originais\Fluviogramas_observados.csv'
path_fluviogramas_sim = 'dados\originais\Fluviogramas_simulados.csv'
df_fluv_obs = pd.read_csv(path_fluviogramas_obs)
df_fluv_sim = pd.read_csv(path_fluviogramas_obs)

print(df_fluv_obs.head())
print(df_fluv_sim.head())

matriz_fluv_obs = df_fluv_obs.values
matriz_fluv_sim = df_fluv_sim.values


# ESTAÇÃO: 38830000

campo_x = 'Data'
campo_y1 = '38830000'
campo_y2 = '1924'

plt.plot(df_fluv_obs[coluna_x], df_fluv_obs[coluna_y1], label='Observada')
plt.plot(df_fluv_sim[coluna_x], df_fluv_sim[coluna_y2], label='Observada')
plt.xlabel('Data')
plt.ylabel('Vazão')
plt.title(f'Fluviograma (observado) - Estação {coluna_y}')
plt.legend()
plt.grid(False)
plt.show()